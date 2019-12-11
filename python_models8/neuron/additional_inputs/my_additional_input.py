from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.additional_inputs import (
    AbstractAdditionalInput)

# TODO: create constants to match the parameter names
MY_ADDITIONAL_INPUT_PARAMETER = "my_additional_input_parameter"
INPUT_CURRENT = "input_current"

# TODO: create units for each parameter
UNITS = {
    MY_ADDITIONAL_INPUT_PARAMETER: "nA",
    INPUT_CURRENT: "nA"
}


class MyAdditionalInput(AbstractAdditionalInput):

    def __init__(
            self,

            # TODO: update the parameters
            my_additional_input_parameter, input_current):

        # TODO: Update the data types - this must match the struct exactly
        super(MyAdditionalInput, self).__init__([
            DataType.S1615,  # my_parameter
            DataType.S1615,  # input_current
        ])

        # TODO: store the parameters
        self._my_additional_input_parameter = my_additional_input_parameter
        self._input_current = input_current

    # TODO: Add getters and setters for the parameters

    @property
    def my_additional_input_parameter(self):
        return self._my_additional_input_parameter

    @my_additional_input_parameter.setter
    def my_additional_input_parameter(self, my_additional_input_parameter):
        self._my_additional_input_parameter = my_additional_input_parameter

    @property
    def input_current(self):
        return self._input_current

    @input_current.setter
    def input_current(self, input_current):
        self._input_current = input_current

    @overrides(AbstractAdditionalInput.get_n_cpu_cycles)
    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    @overrides(AbstractAdditionalInput.add_parameters)
    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[MY_ADDITIONAL_INPUT_PARAMETER] = (
            self._my_additional_input_parameter)

    @overrides(AbstractAdditionalInput.add_state_variables)
    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[INPUT_CURRENT] = self._input_current

    @overrides(AbstractAdditionalInput.get_values)
    def get_values(self, parameters, state_variables, vertex_slice):
        # TODO: Return, in order of the struct, the values from the parameters,
        # state variables, or other
        return [parameters[MY_ADDITIONAL_INPUT_PARAMETER],
                state_variables[INPUT_CURRENT]]

    @overrides(AbstractAdditionalInput.update_values)
    def update_values(self, values, parameters, state_variables):
        # TODO: From the list of values given in order of the struct, update
        # the parameters and state variables
        (_my_parameter, input_current) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!
        state_variables[INPUT_CURRENT] = input_current

    @overrides(AbstractAdditionalInput.has_variable)
    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    @overrides(AbstractAdditionalInput.get_units)
    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
