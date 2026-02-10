from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.threshold_types import AbstractThresholdType
from spynnaker.pyNN.utilities.struct import Struct

# TODO create constants to EXACTLY match the parameter names
# The name of a threshold value
THRESHOLD_VALUE = "threshold_value"
# The name of your custom threshold parameter
THRESHOLD_PARAM = "my_threshold_parameter"


class MyThresholdType(AbstractThresholdType):
    """ A threshold that is a static value.
    """

    def __init__(
            self,

            # TODO: update parameters
            threshold_value, my_threshold_parameter):

        # TODO: Update the data types - this must match the structs exactly
        super().__init__(
            [Struct([
                 (DataType.S1615, THRESHOLD_VALUE),
                 (DataType.S1615,  THRESHOLD_PARAM)])],
            {THRESHOLD_VALUE: "mV", THRESHOLD_PARAM: ""})

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

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[THRESHOLD_PARAM] = self._my_threshold_parameter
        parameters[THRESHOLD_VALUE] = self._threshold_value

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        pass
