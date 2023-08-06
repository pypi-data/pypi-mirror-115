"""Module to extract statistics for the action model learner."""
import csv
import logging
import sys
from typing import NoReturn, List

from pathlib import Path
from pddl.parser import Parser
from pddl.pddl import Domain

from sam_learner.sam_models.types import Trajectory
from sam_learner.core import DomainExporter
from sam_learner import SAMLearner
from sam_learner.visualizations.model_validator import validate_action_model

COLUMN_NAMES = [
	"domain_name",
	"num_trajectories",
	"num_domain_actions",
	"learned_actions_length",
	"domains_equal",
	"avg_trajectories_length",
	"learned_action_names"]


class AMStatisticsExtractor:
	"""Class that is used to extract statistics about the action model learner.

	Attributes:
		logger: the logger for the class.
		working_dir_path: the path to the directory containing the domain and the relevant files.
		expected_domain: the domain that contains all of the actions and the preconditions and
			effects.
		domain_exporter: the class that is able to export the domain to a PDDL file.
	"""

	logger: logging.Logger
	workdir_path: str
	expected_domain: Domain
	domain_exporter: DomainExporter

	def __init__(self, working_dir_path: str, expected_domain_path: str):
		self.logger = logging.getLogger(__name__)
		self.workdir_path = working_dir_path
		self.expected_domain = Parser(expected_domain_path).parse_domain(read_from_file=True)
		self.domain_exporter = DomainExporter()

	def create_trajectories(self) -> List[Trajectory]:
		"""Create the trajectories for the learner.

		:return: the trajectories needed to learn the action model.
		"""
		self.logger.info("Creating the trajectories for the learner to use.")
		learner = SAMLearner(working_directory_path=self.workdir_path)
		return learner.create_trajectories()

	def run_learner(self, complete_statistics: List[dict]) -> NoReturn:
		"""Runs the learner and accumulates the statistics from the run.

		:param complete_statistics: the list of statistics that is to be accumulated.
		"""
		available_trajectories = []
		domain_trajectories = self.create_trajectories()
		(Path(self.workdir_path) / "generated_domains").mkdir(exist_ok=True)
		for trajectory in domain_trajectories:
			statistics = {}
			available_trajectories.append(trajectory)
			learner = SAMLearner(working_directory_path=self.workdir_path)
			assert learner.learned_domain.actions == {}
			self.logger.debug(
				f"Trying to learn the action model with {len(available_trajectories)} trajectories.")
			learned_model = learner.learn_action_model(available_trajectories)
			print("Finished learning the action model from the trajectories!")

			self.write_statistics_data(available_trajectories, learned_model, statistics)
			self.domain_exporter.export_domain(learned_model,
				f"{self.workdir_path}/generated_domains/learned_domain-"
				f"{len(available_trajectories)}-trajectories.pddl")

			complete_statistics.append(statistics)

	def write_statistics_data(self, available_trajectories: List[Trajectory],
							  learned_model: Domain,
							  statistics: dict) -> NoReturn:
		"""Write the statistics of the current execution of the code.

		:param available_trajectories: the available trajectories for the current execution.
		:param learned_model: the domain that was learned with the action model.
		:param statistics: the dictionary that contains the statistics collected during the
			entire program's execution.
		:return:
		"""
		num_trajectories = len(available_trajectories)
		statistics["domain_name"] = self.expected_domain.name
		statistics["num_trajectories"] = num_trajectories
		statistics["num_domain_actions"] = len(self.expected_domain.actions)
		statistics["learned_actions_length"] = len(learned_model.actions)
		statistics["domains_equal"] = validate_action_model(learned_model, self.expected_domain)
		statistics["avg_trajectories_length"] = sum([len(trajec) for trajec in \
													 available_trajectories]) / num_trajectories
		statistics["learned_action_names"] = "/".join([action for action in
													   learned_model.actions])

	def extract_action_model_statistics(self, stats_file_path: str) -> NoReturn:
		"""Extract the statistics and saves them into a CSV file for future usage.

		:param stats_file_path: the path to the file that will contain the statistics.
		"""
		domain_statistics = []
		self.run_learner(domain_statistics)
		with open(stats_file_path, 'wt', newline='') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=COLUMN_NAMES)
			writer.writeheader()
			for data in domain_statistics:
				writer.writerow(data)


if __name__ == '__main__':
	try:
		logging.basicConfig(level=logging.DEBUG)
		args = sys.argv
		workdir_path = args[1]
		domain_path = args[2]
		stats_extractor = AMStatisticsExtractor(workdir_path, domain_path)
		stats_extractor.extract_action_model_statistics(args[3])

	except Exception as e:
		print(e)
