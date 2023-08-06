"""Module to export plans using a remote solver server."""
import logging
import sys
from http import HTTPStatus
from pathlib import Path
from typing import NoReturn

import requests
from requests import Response

SOLVE_AND_VALIDATE_URL = 'http://solver.planning.domains/solve-and-validate'


class RemotePlansGenerator:
	"""Class that uses an external service to generate plans for the learner algorithm.

	Attributes:
		logger: the logger of the class.
	"""

	logger = logging.Logger

	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def export_plan_from_response(self, domain_directory_path: str, problem_file_path: Path,
								  response: Response) -> NoReturn:
		"""Export the plan if exists into a solution file.

		:param domain_directory_path: the directory in which we export the output file to.
		:param problem_file_path: the path to the problem file (used to generate the solution
			file's name.
		:param response: the response that was returned from the solving server.
		"""
		if response.status_code < HTTPStatus.BAD_REQUEST:
			response_data: dict = response.json()
			if "plan" not in response_data["result"]:
				return

			if response_data["result"]["val_status"] == "err":
				self.logger.debug(response_data["result"]["val_stdout"])
				return

			with open(Path(domain_directory_path, f"{problem_file_path.stem}_plan.solution"),
					  "wt") as plan_file:
				self.logger.debug("Solution Found!")
				plan_file.write(
					'\n'.join([action["name"] for action in response_data["result"]["plan"]]))

	def generate_plans(self, domain_directory_path: str) -> NoReturn:
		"""Generate plan files to the problems in the given directory.

		:param domain_directory_path: the directory that contains the domain and the problem
			files that need to be solved.
		"""
		domain_file_path = None
		for file_path in Path(domain_directory_path).glob("*.pddl"):
			if "domain" in file_path.name:
				domain_file_path = file_path
				continue

			if domain_file_path is not None:
				self.logger.info(f"Solving the problem {file_path.stem}")
				with open(domain_file_path, "rt") as domain_file, open(file_path,
																	   "rt") as problem_file:
					data = {"domain": domain_file.read(), "problem": problem_file.read()}
					response: Response = requests.post(SOLVE_AND_VALIDATE_URL, verify=False,
													   json=data)

					self.export_plan_from_response(domain_directory_path, file_path, response)


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	directory_path = sys.argv[1]
	RemotePlansGenerator().generate_plans(directory_path)
