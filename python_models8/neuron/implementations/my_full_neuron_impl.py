from data_specification.enums.data_type import DataType
from spinn_front_end_common.utilities.constants import BYTES_PER_WORD
from spynnaker.pyNN.utilities.struct import Struct
from spynnaker.pyNN.models.neuron.implementations import (
    AbstractNeuronImpl, RangedDictVertexSlice)

# TODO: Add names for parameters and state variables
THRESHOLD = "threshold"
V = "v"
EXC_INPUT = "exc_input"
INH_INPUT = "inh_input"

# TODO: Update the units for the parameters and state variables
UNITS = {
    THRESHOLD: "mV",
    V: "mV",
    EXC_INPUT: "nA",
    INH_INPUT: "nA"
}


class MyFullNeuronImpl(AbstractNeuronImpl):

    def __init__(self,

                 # TODO: add model parameters and state variables
                 threshold, v, exc_input, inh_input):

        # TODO: Store the variables
        self._threshold = threshold
        self._v = v
        self._exc_input = exc_input
        self._inh_input = inh_input

        # TODO: Store a struct to make other operations easier
        self._struct = Struct([
            DataType.S1615,  # inputs[0]
            DataType.S1615,  # inputs[1]
            DataType.S1615,  # v
            DataType.S1615   # threshold
        ])

    # TODO: Add getters and setters for the parameters

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        self._threshold = threshold

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v

    @property
    def exc_input(self):
        return self._exc_input

    @exc_input.setter
    def exc_input(self, exc_input):
        self._exc_input = exc_input

    @property
    def inh_input(self):
        return self._inh_input

    @inh_input.setter
    def inh_input(self, inh_input):
        self._inh_input = inh_input

    @property
    def model_name(self):
        # TODO: Update the name
        return "MyFullNeuronImpl"

    @property
    def binary_name(self):
        # TODO: Update the binary name
        return "my_full_neuron_impl.aplx"

    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Update (or guess) the number of CPU cycles
        return 10 * n_neurons

    def get_dtcm_usage_in_bytes(self, n_neurons):
        # This is extracted from the struct, so no need to update
        return self._struct.get_size_in_whole_words(n_neurons) * BYTES_PER_WORD

    def get_sdram_usage_in_bytes(self, n_neurons):
        # This is extracted from the struct, so no need to update
        return self._struct.get_size_in_whole_words(n_neurons) * BYTES_PER_WORD

    def get_global_weight_scale(self):
        # TODO: Update if a weight scale is required
        return 1.0

    def get_n_synapse_types(self):
        # TODO: Update to the number of synapse types your model uses
        # (this is the inputs array in this model)
        return 2

    def get_synapse_id_by_target(self, target):
        # TODO: Update with the names that are allowed on a PyNN synapse
        # receptor_type and match up with indices
        if target == "excitatory":
            return 0
        elif target == "inhibitory":
            return 1
        raise ValueError("Unknown target {}".format(target))

    def get_synapse_targets(self):

        # TODO: Update with the names that are allowed on a PyNN synapse
        # receptor_type
        return ["excitatory", "inhibitory"]

    def get_recordable_variables(self):
        # TODO: Update with the names of state variables that can be recorded
        return ["v"]

    def get_recordable_data_types(self):
        # TODO: Update with the names and recorded types of the state variables
        return {"v": DataType.S1615}

    def get_recordable_units(self, variable):
        # TODO: Update with the appropriate units for variables
        if variable != "v":
            raise ValueError("Unknown variable {}".format(variable))
        return "mV"

    def get_recordable_variable_index(self, variable):
        # TODO: Update with the index in the recorded_variable_values array
        # that the given variable will be recorded in to
        if variable != "v":
            raise ValueError("Unknown variable {}".format(variable))
        return 0

    def is_recordable(self, variable):
        # TODO: Update to identify variables that can be recorded
        return variable == "v"

    def add_parameters(self, parameters):
        # TODO: Write the parameter values
        parameters[THRESHOLD] = self._threshold

    def add_state_variables(self, state_variables):
        # TODO: Write the state variable values
        state_variables[V] = self._v
        state_variables[EXC_INPUT] = self._exc_input
        state_variables[INH_INPUT] = self._inh_input

    def get_data(self, parameters, state_variables, vertex_slice):
        # TODO: get the data in the appropriate form to match the struct
        values = [state_variables[EXC_INPUT],
                  state_variables[INH_INPUT],
                  state_variables[V],
                  parameters[THRESHOLD]]
        return self._struct.get_data(
            values, vertex_slice.lo_atom, vertex_slice.n_atoms)

    def read_data(
            self, data, offset, vertex_slice, parameters, state_variables):
        # TODO: Extract items from the data to be updated
        (exc_input, inh_input, v, _threshold) = self._struct.read_data(
            data, offset, vertex_slice.n_atoms)
        new_offset = offset + self._struct.get_size_in_whole_words(
            vertex_slice.n_atoms)
        variables = RangedDictVertexSlice(state_variables, vertex_slice)

        variables[EXC_INPUT] = exc_input
        variables[INH_INPUT] = inh_input
        variables[V] = v

        return new_offset

    def get_units(self, variable):
        # This uses the UNITS dict so shouldn't need to be updated
        return UNITS[variable]

    @property
    def is_conductance_based(self):
        # TODO: Update if uses conductance
        return False
