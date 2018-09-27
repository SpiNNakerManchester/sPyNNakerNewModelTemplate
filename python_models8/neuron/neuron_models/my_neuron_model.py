from pacman.executor.injection_decorator import inject_items
from spynnaker.pyNN.models.neuron.neuron_models import AbstractNeuronModel
from data_specification.enums import DataType

# TODO: create constants to match the parameter names
I_OFFSET = "i_offset"
MY_NEURON_PARAMETER = "my_neuron_parameter"
V = "v"

# TODO: create units for each parameter
UNITS = {
    I_OFFSET: "nA",
    MY_NEURON_PARAMETER: "mV",
    V: "mV"
}


class MyNeuronModel(AbstractNeuronModel):
    def __init__(
            self,

            # TODO: update the parameters and state variables
            i_offset, my_neuron_parameter, v):

        # TODO: Update the data types - this must match the structs exactly
        super(MyNeuronModel, self).__init__(
            data_types=[
                DataType.S1615,   # v
                DataType.S1615,   # i_offset
                DataType.S1615],  # my_parameter
            global_data_types=[
                DataType.UINT32   # machine_time_step
            ])

        # TODO: Store any parameters and state variables
        self._i_offset = i_offset
        self._my_neuron_parameter = my_neuron_parameter
        self._v = v

    # TODO: Add getters and setters for the parameters

    @property
    def i_offset(self):
        return self._i_offset

    @i_offset.setter
    def i_offset(self, i_offset):
        self._i_offset = i_offset

    @property
    def my_neuron_parameter(self):
        return self._my_neuron_parameter

    @my_neuron_parameter.setter
    def my_neuron_parameter(self, my_neuron_parameter):
        self._my_neuron_parameter = my_neuron_parameter

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v

    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[I_OFFSET] = self._i_offset
        parameters[MY_NEURON_PARAMETER] = self._my_neuron_parameter

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[V] = self._v

    def get_values(self, parameters, state_variables, vertex_slice):
        # TODO: Return, in order of the struct, the values from the parameters,
        # state variables, or other
        return [state_variables[V],
                parameters[I_OFFSET],
                parameters[MY_NEURON_PARAMETER]]

    @inject_items({"machine_time_step": "MachineTimeStep"})
    def get_global_values(self, machine_time_step):
        return [machine_time_step]

    def update_values(self, values, parameters, state_variables):
        # TODO: From the list of values given in order of the struct, update
        # the parameters and state variables
        (v, _i_offset, _my_parameter) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!
        state_variables[V] = v

    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
