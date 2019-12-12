from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.threshold_types import AbstractThresholdType

# TODO create constants to EXACTLY match the parameter names
# The name of a threshold value
THRESHOLD_VALUE = "threshold_value"
# The name of your custom threshold parameter
THRESHOLD_PARAM = "my_threshold_parameter"

# TODO: create units for each parameter
UNITS = {
    THRESHOLD_VALUE: "mV",
    THRESHOLD_PARAM: ""
}


class MyThresholdType(AbstractThresholdType):
    """ A threshold that is a static value.
    """

    def __init__(
            self,

            # TODO: update parameters
            threshold_value, my_threshold_parameter):

        # TODO: Update the data types - this must match the structs exactly
        super(MyThresholdType, self).__init__([
            DataType.S1615,  # threshold_value
            DataType.S1615,  # my_param
        ])

        # TODO: Store any parameters
        self._threshold_value = threshold_value
        self._my_threshold_parameter = my_threshold_parameter

    # TODO: Add getters and setters for the parameters

    @property
    def threshold_value(self):
        return self._threshold_value

    @threshold_value.setter
    def threshold_value(self, threshold_value):
        self._threshold_value = threshold_value

    @property
    def my_threshold_parameter(self):
        return self._my_threshold_parameter

    @my_threshold_parameter.setter
    def my_threshold_parameter(self, my_threshold_parameter):
        self._my_threshold_parameter = my_threshold_parameter

    @overrides(AbstractThresholdType.get_n_cpu_cycles)
    def get_n_cpu_cycles(self, n_neurons):
        # TODO: Calculate (or guess) the CPU cycles
        return 10 * n_neurons

    @overrides(AbstractThresholdType.add_parameters)
    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[THRESHOLD_PARAM] = self._my_threshold_parameter
        parameters[THRESHOLD_VALUE] = self._threshold_value

    @overrides(AbstractThresholdType.add_state_variables)
    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        pass

    @overrides(AbstractThresholdType.get_values)
    def get_values(self, parameters, state_variables, vertex_slice):
        # TODO: Return, in order of the struct, the values from the parameters,
        # state variables, or other
        return [parameters[THRESHOLD_VALUE],
                parameters[THRESHOLD_PARAM]]

    @overrides(AbstractThresholdType.update_values)
    def update_values(self, values, parameters, state_variables):
        # TODO: From the list of values given in order of the struct, update
        # the parameters and state variables
        (_threshold_value, _threshold_param) = values

        # NOTE: If you know that the value doesn't change, you don't have to
        # assign it (hint: often only state variables are likely to change)!

    @overrides(AbstractThresholdType.has_variable)
    def has_variable(self, variable):
        # This works from the UNITS dict, so no changes are required
        return variable in UNITS

    @overrides(AbstractThresholdType.get_units)
    def get_units(self, variable):
        # This works from the UNITS dict, so no changes are required
        return UNITS[variable]
