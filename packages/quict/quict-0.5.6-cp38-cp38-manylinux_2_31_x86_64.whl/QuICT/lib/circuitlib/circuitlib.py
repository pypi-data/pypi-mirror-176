import os
import re

from QuICT.lib.qasm.exceptions import QasmError
from QuICT.tools.interface import OPENQASMInterface


class CircuitLib:
    """
    A class handling QuICT circuit library.
    """

    @classmethod
    def _load_qasm(cls, filename):
        """
        Load a qasm file.
        """
        qasm = OPENQASMInterface.load_file(filename)
        if not qasm.valid_circuit:
            raise QasmError("Missing input file")
        return qasm.circuit

    @classmethod
    def _load_all(cls, filename):
        """
        Load all qasm files under `filename`
        """
        circuit_all = []
        for root, dirs, files in os.walk(filename):
            for file in files:
                circuit_all.append(cls._load_qasm(os.path.join(filename, file)))
        return circuit_all

    @classmethod
    def load_template_circuit(cls, max_width=None, max_size=None, max_depth=None):
        """
        Load template circuits in QuICT circuit library. A template will be loaded if
        it satisfies the following restrictions:
            1. its number of qubits <= `max_width`,
            2. its number of gates <= `max_size`,
            3. its depth <= `max_depth`.

        Restrictions will be ignored if not specified.

        Args:
            max_width(int): max number of qubits
            max_size(int): max number of gates
            max_depth(int): max depth

        Returns:
            list: a list of required circuits
        """

        if max_width is None:
            max_width = float('inf')
        if max_size is None:
            max_size = float('inf')
        if max_depth is None:
            max_depth = float('inf')

        circuit_list = []
        path = os.path.join(os.path.dirname(__file__), 'circuit_qasm', 'template')

        pat = '^template_w([0-9]+)_s([0-9]+)_d([0-9]+)_([0-9]+).qasm$'
        for qasm in filter(lambda x: x.startswith('template') and x.endswith('.qasm'),
                           os.listdir(path)):

            re_list = re.match(pat, qasm).groups()
            if len(re_list) >= 4:
                n, m, d, _ = [int(x) for x in re_list]
                if n <= max_width and m <= max_size and d <= max_depth:
                    circ = cls._load_qasm(os.path.join(path, qasm))
                    circuit_list.append(circ)
            else:
                print(f'WARNING: {os.path.join(path, qasm)} bad naming.')

        return circuit_list

    @classmethod
    def load_circuit(cls, name="template", *args):

        """

        name: "template", "random", "algorithm", "experiment"

        *args:

                template:   args[0]: qubit_num, upper bound of qubit number
                                     of templates
                            args[1]: size, upper bound of size of templates
                            args[2]: depth, upper bound of depth of templates

                random:     args[0]: circuit_type ("ctrl_diag"/"ctrl_unitary"
                                                    /"diag"/"qft"/"single_bit"
                                                    /"unitary"),
                                     type of random circuits
                            args[1]: qubit number (list/int), get a list of
                                     circuits (a single circuit) with given
                                     qubit numbers

                algorithm:  args[0]: circuit_type ("QFT"/"Grover"/"Supermacy"),
                                     type of algorithm circuits
                            args[1]: qubit number (list/int), get a list of
                                     circuits (a single circuit) with given
                                     qubit numbers

                experiment: args[0]: circuit_type("Mapping"/"Adder"), type of
                                     experiment circuits
                            args[1]: (for Adder)   qubit number (list/int), get
                                                   a list of circuits (a single
                                                   circuit) with given qubit
                                                   numbers
                                     (for Mapping) mapping_name, get all
                                                   mapping circuits under the
                                                   same qubit mapping type

        """

        para = args
        circuit_list = []
        filename = os.path.dirname(__file__) + '/circuit_qasm/' + name

        if name == "template":
            # get all templates satisfying <=bit_num & <=size & <=depth
            circuit_list = cls.load_template_circuit(*para)

        elif name == "random":

            # get all random circuits

            filename += '/' + para[0]
            if isinstance(para[1], int):
                random_list = [para[1]]
            else:
                random_list = para[1]
            for list_name in random_list:
                filesname = filename + '/' + str(list_name) + ".qasm"
                circuit = cls._load_qasm(filesname)
                if circuit is not None:
                    circuit_list.append(circuit)

        elif name == "algorithm":

            # get all algorithm circuits

            filename += '/' + para[0]
            al_dic = {"QFT": "/qft_", "Grover": "/grover_", "Supremacy": "/"}
            if para[0] in al_dic:
                if isinstance(para[1], int):
                    algorithm_list = [para[1]]
                else:
                    algorithm_list = para[1]
                for list_name in algorithm_list:
                    filesname = filename + al_dic[para[0]]
                    filesname += str(list_name) + ".qasm"
                    circuit = cls._load_qasm(filesname)
                    if circuit is not None:
                        circuit_list.append(circuit)
            else:
                filename = ""

        elif name == "experiment":

            # get all experiment circuits

            filename += '/' + para[0]
            if para[0] == "Mapping":
                filename += '/' + para[1]
                circuit = cls._load_all(filename)
                if circuit is not None:
                    circuit_list.append(circuit)
            elif para[0] == "Adder":
                filename += '/adder_n'
                if isinstance(para[1], int):
                    adder_list = [para[1]]
                else:
                    adder_list = para[1]
                for list_name in adder_list:
                    filesname = filename + str(list_name) + ".qasm"
                    circuit = cls._load_qasm(filesname)
                    if circuit is not None:
                        circuit_list.append(circuit)
            else:
                filename = ""
        else:
            filename = ""
        return circuit_list
