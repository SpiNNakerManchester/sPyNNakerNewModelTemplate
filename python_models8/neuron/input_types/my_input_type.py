from spynnaker.pyNN.models.neuron.input_types import AbstractInputType
from data_specification.enums.data_type import DataType

# TODO create constants to match the parameter names
MY_MULTIPLICATOR = "my_multiplicator"
MY_INPUT_PARAMETER = "my_input_parameter"

# TODO create units for each parameter
UNITS = {
    MY_MULTIPLICATOR: "",
    MY_INPUT_PARAMETER: "mA"
}


class MyInputType(AbstractInputType):

    def __init__(
            self,

            # TODO: update the parameters
            my_multiplicator,
            my_input_parameter):

        # TODO: Update the data types
        super().__init__([
            DataType.S1615,  # my_multiplicator
            DataType.S1615   # my_input_parameter
        ])

        # TODO: store the parameters
        self._my_multiplicator = my_multiplicator
        self._my_input_parameter = my_input_parameter

    # TODO: Add getters and setters for the parameters

    @property
    def my_multiplicator(self):
        return self._my_multiplicator

    @property
    def my_input_parameter(self):
        return self._my_input_parameter

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self._my_multiplicator = my_multiplicator

    @my_input_parameter.setter
    def my_input_parameter(self, my_input_parameter):
        self._my_input_parameter = my_input_parameter

    def get_global_weight_scale(self):
        return 1.0

    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[MY_INPUT_PARAMETER] = self._my_input_parameter

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[MY_MULTIPLICATOR] = self._my_multiplicator

    def get_values(self, parameters, state_variables, vertex_slice, ts):
        # TODO: Return, in order of the struct, the values from the parameters,
        # state variables, or other
        return [state_variables[MY_MULTIPLICATOR],
                parameters[MY_INPUT_PARAMETER]]

    def update_values(self, values, parameters, state_variables):
        # TODO: From the list of values given in order of the struct, update
        # the parameters and state variables
        (_my_input_parameter, my_multiplicator) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!
        state_variables[MY_MULTIPLICATOR] = my_multiplicator

    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
