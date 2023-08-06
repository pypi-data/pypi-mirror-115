"""This module exports the domain object to a domain file."""
from collections import defaultdict
from pathlib import Path
from typing import NoReturn, List, Dict

from pddl.pddl import Domain, Action, Predicate, Type


class DomainExporter:
	"""Class that is able to export a domain to a correct PDDL file."""

	def write_action_preconditions(self, predicates: List[Predicate]) -> str:
		"""Writes the predicates formatted according to the domain file format.

		:param predicates:
		:return:
		"""
		formatted_preconditions = "(and {content})"
		action_predicates = self._write_positive_predicates(predicates)
		return formatted_preconditions.format(content=" ".join(action_predicates))

	def _write_positive_predicates(self, predicates: List[Predicate]) -> List[str]:
		"""

		:param predicates:
		:return:
		"""
		action_predicates = []
		for predicate in predicates:
			predicate_formatted_signature = " ".join([f"{name}" for name, _ in predicate.signature])
			predicate_str = f"({predicate.name} - {predicate_formatted_signature})"
			action_predicates.append(predicate_str)

		return action_predicates

	def _write_negative_predicates(self, predicates: List[Predicate]) -> List[str]:
		"""

		:param predicates:
		:return:
		"""
		action_predicates = []
		for predicate in predicates:
			predicate_formatted_signature = " ".join([f"{name}" for name, _ in predicate.signature])
			predicate_str = f"(not ({predicate.name} - {predicate_formatted_signature}))"
			action_predicates.append(predicate_str)

		return action_predicates

	def write_action_effects(self, add_effects: List[Predicate],
							 delete_effects: List[Predicate]) -> str:
		"""

		:param add_effects:
		:param delete_effects:
		:return:
		"""
		formatted_preconditions = "(and {content})"
		action_predicates = self._write_positive_predicates(add_effects)
		action_predicates + self._write_negative_predicates(delete_effects)
		return formatted_preconditions.format(content=" ".join(action_predicates))

	def write_action(self, action: Action) -> str:
		"""Write the action formatted string from the action data.

		:param action: The action that needs to be formatted into a string.
		:return: the string format of the action.
		"""
		action_params = " ".join([f"{name} - {types[0]}" for name, types in action.signature])
		action_preconds = self.write_action_preconditions(action.precondition)
		action_effects = self.write_action_effects(action.effect.addlist, action.effect.dellist)
		return f"(:action {action.name}\n" \
			   f":parameters ({action_params})\n" \
			   f":precondition {action_preconds}\n" \
			   f":effect {action_effects})\n" \
			   f"\n"

	def write_predicates(self, predicates: Dict[str, Predicate]) -> str:
		"""

		:param predicates:
		:return:
		"""
		predicates_str = "(:predicates\n{predicates})\n\n"
		predicates_strings = []
		for predicate_name, predicate in predicates.items():
			predicate_params = " ".join(
				[f"{name} - {types[0]}" for name, types in predicate.signature])
			predicates_strings.append(f"\t({predicate_name} {predicate_params})")

		return predicates_str.format(predicates="\n".join(predicates_strings))

	def write_constants(self, constants: Dict[str, Type]) -> str:
		"""TODO: Complete this if there is a domain that contains constants."""
		pass

	def write_types(self, types: Dict[str, Type]) -> str:
		"""

		:param types:
		:return:
		"""
		types_str = "(:types\n{types_content})\n"
		sorted_types = defaultdict(list)
		for type_name, pddl_type in types.items():
			sorted_types[pddl_type.name].append(type_name)

		types_content = []
		for pddl_type_name, subtypes in sorted_types.items():
			subtypes_str = " ".join(subtypes)
			types_content.append(f"\t{subtypes_str} - {pddl_type_name}")

		return types_str.format(types_content="\n".join(types_content))

	def export_domain(self, domain: Domain, export_path: Path) -> NoReturn:
		"""Export the domain object to a correct PDDL file.

		:param domain:
		:param export_path:
		"""
		domain_types = self.write_types(domain.types)
		domain_headers = f"(define (domain {domain.name})\n" \
						 "(:requirements :typing)\n\n" \
						 f"{domain_types}\n" \
						 "{domain_content})"
		domain_content = self.write_predicates(domain.predicates)
		for action in domain.actions.values():
			domain_content += self.write_action(action)

		with open(export_path, "wt") as export_domain_file:
			export_domain_file.write(domain_headers.format(domain_content=domain_content))
