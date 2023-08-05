from functools import cached_property
from itertools import chain
from typing import List

from QuICT.core import Circuit

from .matching_dag_circuit import Match, MatchingDAGCircuit, MatchingDAGNode

GATE_COST = {
    'id': 0, 'x': 1, 'y': 1, 'z': 1, 'h': 1, 't': 1, 'tdg': 1, 's': 1, 'sdg': 1,
    'u1': 1, 'u2': 2, 'u3': 2, 'rx': 1, 'ry': 1, 'rz': 1, 'r': 2, 'cx': 2,
    'cy': 4, 'cz': 4, 'ch': 8, 'swap': 6, 'iswap': 8, 'rxx': 9, 'ryy': 9,
    'rzz': 5, 'rzx': 7, 'ms': 9, 'cu3': 10, 'crx': 10, 'cry': 10, 'crz': 10,
    'ccx': 21, 'rccx': 12, 'c3x': 96, 'rc3x': 24, 'c4x': 312, 'p': 1
}


class Substitution:
    """
    Class for a substitution.
    """
    def __init__(self,
                 circuit: MatchingDAGCircuit,
                 template: MatchingDAGCircuit,
                 match: Match):
        """
        Args:
            circuit(MatchingDAGCircuit): the circuit to match
            template(MatchingDAGCircuit): the template to be matched
            match(Match): the matching for this substitution
        """
        self.circuit = circuit
        self.template = template
        self.match = match

    @cached_property
    def cost(self):
        """
        Returns:
            int: Cost reduced if when substitution is done.
        """
        old_nodes = self.match.template_nodes
        new_nodes = set(range(self.template.size)) - old_nodes
        old_cost = sum(GATE_COST[self.template.get_node(n).name] for n in old_nodes)
        new_cost = sum(GATE_COST[self.template.get_node(n).name] for n in new_nodes)
        return old_cost - new_cost

    @cached_property
    def pred(self):
        """
        Returns:
            List[int]: predecessors (direct and indirect) of matched nodes in the circuit
        """
        return sorted(self.pred_set)

    @cached_property
    def pred_set(self):
        """
        Returns:
            Set[int]: predecessors (direct and indirect) of matched nodes in the circuit
        """

        return self.circuit.all_predecessors(self.match.circuit_nodes)

    def cmp_with(self, other):
        """
        Whether `self` comes before `other`. Namely, whether any matched node of
        `self` is a predecessor of matched nodes of `other`.

        Args:
            other(Substitution): the other substitution to compare

        Returns:
            int: -1 if `self` comes before `other`. Otherwise 1.
        """

        assert isinstance(other, Substitution)
        return -1 if self.match.circuit_nodes & other.pred_set else 1

    def get_substitution(self):
        """
        Get the substitution of circuit for the matching.
        """

        pred = self.template.all_predecessors(self.match.template_nodes)
        succ = set(self.template.nodes()) - self.match.template_nodes - pred

        circ = Circuit(self.circuit.width)
        for node_id in chain(sorted(pred, reverse=True), sorted(succ, reverse=True)):
            # inverse every gates not matched
            node: MatchingDAGNode = self.template.get_node(node_id)
            qubits = list([self.match.qubit_mapping[i] for i in node.qargs])
            node.gate.inverse().copy() | circ(qubits)
        return circ


class TemplateSubstitution:

    @classmethod
    def _sort_sub_list(cls, sub_list: List[Substitution]):
        """
        Sort all substitution in topological order.
        """
        res = []
        while len(sub_list) > 0:
            # find a sub that is not preceded by any other sub
            found = -1
            for idx, cur in enumerate(sub_list):
                if cur is not None and all(s.cmp_with(cur) > 0 for s in sub_list):
                    found = idx
                    break

            # add the found sub to the resulting list
            res.append(sub_list[found])
            sub_list = sub_list[:found] + sub_list[found + 1:]

        return res

    @classmethod
    def _calc_sub_list(cls,
                       circuit: MatchingDAGCircuit,
                       template: MatchingDAGCircuit,
                       match_list: List[Match]):
        """
        Greedily calculate a maximal and compatible sub list for found matches.
        """

        all_subs = [Substitution(circuit, template, m) for m in match_list]

        sub_list = []
        visited_nodes = set()
        # enumerate subs that have positive `cost` in decreasing order
        for sub in sorted(filter(lambda s: s.cost > 0, all_subs),
                          key=lambda s: s.cost,
                          reverse=True):
            cur_nodes = sub.match.circuit_nodes

            # subs must not intersect
            if visited_nodes & cur_nodes:
                continue

            # if two subs both have some node precede the other, it is not valid
            flag_intersect = False
            for other_sub in sub_list:
                if (other_sub.pred_set & cur_nodes) and \
                        (sub.pred_set & other_sub.match.circuit_nodes):
                    flag_intersect = True
                    break

            if not flag_intersect:
                visited_nodes |= cur_nodes
                sub_list.append(sub)

        return cls._sort_sub_list(sub_list)

    @classmethod
    def execute(cls,
                circuit: MatchingDAGCircuit,
                template: MatchingDAGCircuit,
                match_list: List[Match]):

        sub_list = cls._calc_sub_list(circuit, template, match_list)

        new_circ = Circuit(circuit.width)
        visited_nodes = set()

        # Given a sorted valid sub list, every time append unvisited predecessors to the
        # resulting circuit and then append the inverse circuit of the sub.
        for sub in sub_list:
            for node_id in filter(lambda x: x not in visited_nodes, sub.pred):
                node: MatchingDAGNode = circuit.get_node(node_id)
                new_circ.append(node.gate.copy())

            new_circ.extend(sub.get_substitution().gates)

            visited_nodes.update(sub.pred)
            visited_nodes.update(sub.match.circuit_nodes)

        for node_id in filter(lambda x: x not in visited_nodes, circuit.nodes()):
            node: MatchingDAGNode = circuit.get_node(node_id)
            new_circ.append(node.gate.copy())

        return MatchingDAGCircuit(new_circ)
