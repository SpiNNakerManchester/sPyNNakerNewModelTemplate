import numpy
from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.synapse_types import AbstractSynapseType

# TODO: create constants to match the parameter names
EX_SYNAPSE = 'my_ex_synapse_parameter'
IN_SYNAPSE = 'my_in_synapse_parameter'
EXC_INIT = 'my_exc_init'
INH_INIT = 'my_inh_init'

# TODO: create units for each parameter
UNITS = {
    EX_SYNAPSE: "mV",
    IN_SYNAPSE: 'mV',
    EXC_INIT: "uS",
    INH_INIT: "uS"}


class MySynapseType(AbstractSynapseType):
    def __init__(
            self,

            # TODO: update the parameters
            my_ex_synapse_parameter,
            my_in_synapse_parameter,
            my_exc_init,
            my_inh_init):

        # TODO: Update the data types - this must match the struct exactly
        super().__init__([
            DataType.U032,  # my_exc_decay
            DataType.U032,  # my_exc_init
            DataType.U032,  # my_inh_decay
            DataType.U032,  # my_inh_init
            DataType.S1615,  # my_input_buffer_excitatory_value
            DataType.S1615   # my_input_buffer_inhibitory_value;
        ])

        # TODO: Store the parameters
        self._my_ex_synapse_parameter = my_ex_synapse_parameter
        self._my_in_synapse_parameter = my_in_synapse_parameter
        self._my_exc_init = my_exc_init
        self._my_inh_init = my_inh_init

    # TODO: Add any getters and setters for new parameters

    @property
    def my_ex_synapse_parameter(self):
        return self._my_ex_synapse_parameter

    @my_ex_synapse_parameter.setter
    def my_ex_synapse_parameter(self, my_ex_synapse_parameter):
        self._my_ex_synapse_parameter = my_ex_synapse_parameter

    @property
    def my_in_synapse_parameter(self):
        return self._my_in_synapse_parameter

    @my_in_synapse_parameter.setter
    def my_in_synapse_parameter(self, my_in_synapse_parameter):
        self._my_in_synapse_parameter = my_in_synapse_parameter

    @property
    def my_exc_init(self):
        return self._my_exc_init

    @my_exc_init.setter
    def my_exc_init(self, my_exc_init):
        self._my_exc_init = my_exc_init

    @property
    def my_inh_init(self):
        return self._my_inh_init

    @my_inh_init.setter
    def my_inh_init(self, my_inh_init):
        self._my_inh_init = my_inh_init

    @overrides(AbstractSynapseType.get_n_synapse_types)
    def get_n_synapse_types(self):
        # TODO: Update with the number of supported synapse types
        return 2

    @overrides(AbstractSynapseType.get_synapse_id_by_target)
    def get_synapse_id_by_target(self, target):
        # TODO: update the mapping from name to ID
        if target == "excitatory":
            return 0
        elif target == "inhibitory":
            return 1
        return None

    @overrides(AbstractSynapseType.get_synapse_targets)
    def get_synapse_targets(self):
        # TODO: update to return the same names as above
        return "excitatory", "inhibitory"

    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[EX_SYNAPSE] = self._my_ex_synapse_parameter
        parameters[IN_SYNAPSE] = self._my_in_synapse_parameter

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[EXC_INIT] = self._my_exc_init
        state_variables[INH_INIT] = self._my_inh_init

    def get_values(self, parameters, state_variables, vertex_slice, ts):
        # TODO: Return, in order of the struct, the values from the parameters,
        # state variables, or other
        tsfloat = float(ts) / 1000.0
        decay = lambda x: numpy.exp(-tsfloat / x)  # noqa E731
        init = lambda x: (x / tsfloat) * (1.0 - numpy.exp(-tsfloat / x))  # noqa E731
        return [parameters[EX_SYNAPSE].apply_operation(decay),
                parameters[EX_SYNAPSE].apply_operation(init),
                parameters[IN_SYNAPSE].apply_operation(decay),
                parameters[IN_SYNAPSE].apply_operation(init),
                state_variables[EXC_INIT], state_variables[INH_INIT]]

    def update_values(self, values, parameters, state_variables):
        # TODO: From the list of values given in order of the struct, update
        # the parameters and state variables
        (_ex_decay, _ex_init, _in_decay, _in_init, exc_init, inh_init) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!
        state_variables[EXC_INIT] = exc_init
        state_variables[INH_INIT] = inh_init

    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
