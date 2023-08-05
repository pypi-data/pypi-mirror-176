from typing import List

from QuICT.core import Circuit
from QuICT.lib.circuitlib import CircuitLib
from QuICT.qcda.optimization.template_optimization.template_matching.template_matching import (
    MatchingDAGCircuit, TemplateMatching
)
from QuICT.qcda.optimization.template_optimization.template_matching.template_substitution import TemplateSubstitution


class TemplateOptimization(object):
    """
    Template optimization algorithm.

    [1] Iten, R., Moyard, R., Metger, T., Sutter, D. and Woerner, S., 2020.
    Exact and practical pattern matching for quantum circuit optimization.
    `arXiv:1909.05270 <https://arxiv.org/abs/1909.05270>`
    """

    def __init__(
            self,
            template_list=None,
            heuristics_qubits_param=None,
            heuristics_backward_param=None
    ):
        """
        Heuristic qubit parameters `heuristics_qubits_param` is in the form [cnt] where `cnt` is
        the number of additional qubits explored when enumerating the qubit mapping (recommended
        value is 1).

        Heuristic backward match parameter `heuristics_backward_param` is in the form [D, W].
        Backward match will prune the search tree when depth=k*D (k = 1, 2, ...) and at most W
        maximal matching scenarios will survive (recommended value is [3, 1]).

        Above two heuristic algorithms will be executed only when the corresponding parameter is
        specified.

        Args:
            template_list(List[Circuit]): the list of templates used
                (by default all templates of 2 gates in CircuitLib are used).
            heuristics_qubits_param(List[int]): Heuristic qubit parameters
            heuristics_backward_param(List[int]): Heuristic backward match parameter
        """

        self.template_list = template_list
        self.heuristics_qubits_param = heuristics_qubits_param
        self.heuristics_backward_param = heuristics_backward_param

        if self.template_list is None:
            self.template_list = CircuitLib.load_template_circuit(max_size=2)

    def execute(self, circuit):
        """
        Execute template optimization algorithm.

        Args:
            circuit(Circuit): the circuit to be optimized

        Returns:
            Circuit: the optimized circuit
        """

        circ_dag = MatchingDAGCircuit(circuit)

        for template in self.template_list:
            template_dag = MatchingDAGCircuit(template)

            if template_dag.width > circ_dag.width:
                continue

            matches = TemplateMatching.execute(
                circ_dag,
                template_dag,
                self.heuristics_qubits_param,
                self.heuristics_backward_param
            )

            circ_dag = TemplateSubstitution.execute(circ_dag, template_dag, matches)

        return circ_dag.get_circuit()
