from spynnaker.pyNN.models.neural_properties import NeuronParameter
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.threshold_types import AbstractThresholdType
from spynnaker.pyNN.utilities.ranged import SpynnakerRangeDictionary
from enum import Enum
from spinn_utilities.overrides import overrides

# TODO create constants to EXACTLY match the parameter names
#! The name of a threshold value
THRESHOLD_VALUE_NAME = "threshold_value"
#! The name of your custom threshold parameter
THRESHOLD_PARAM_NAME = "my_threshold_parameter"


class _MY_THRESHOLD_TYPES(Enum):

    THRESHOLD_VALUE = (1, DataType.S1615)
    MY_THRESHOLD_PARAMETER = (2, DataType.S1615)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


class MyThresholdType(AbstractThresholdType):
    """ A threshold that is a static value.
    """

    def __init__(
            self, n_neurons,
            # TODO: update parameters
            threshold_value, my_threshold_parameter):
        self._n_neurons = n_neurons
        self._data = SpynnakerRangeDictionary(size=n_neurons)

        # TODO: Store any parameters
        self._data[THRESHOLD_VALUE_NAME] = threshold_value
        self._data[THRESHOLD_PARAM_NAME] = my_threshold_parameter

    # TODO: Add getters and setters for the parameters

    @property
    def threshold_value(self):
        return self._data[THRESHOLD_VALUE_NAME]

    @threshold_value.setter
    def threshold_value(self, threshold_value):
        self._data.set_value(
            ey=THRESHOLD_VALUE_NAME, value=threshold_value)

    @property
    def my_threshold_parameter(self):
        return self._data[THRESHOLD_PARAM_NAME]

    @my_threshold_parameter.setter
    def my_threshold_parameter(self, my_threshold_parameter):
        self._data.set_value(
            key=THRESHOLD_PARAM_NAME, value=my_threshold_parameter)

    @overrides(AbstractThresholdType.get_n_threshold_parameters)
    def get_n_threshold_parameters(self):
        # TODO: update to return the number of parameters
        # Note: This must match the number of values in the threshold_type_t
        # data structure in the C code
        return 2

    @overrides(AbstractThresholdType.get_threshold_parameters)
    def get_threshold_parameters(self):
        # TODO: update to return the parameters
        # Note: The order of the parameters must match the order in the
        # threshold_type_t data structure in the C code
        return [
            NeuronParameter(
                self._data[THRESHOLD_VALUE_NAME],
                _MY_THRESHOLD_TYPES.THRESHOLD_VALUE.data_type),
            NeuronParameter(
                self._data[THRESHOLD_PARAM_NAME],
                _MY_THRESHOLD_TYPES.MY_THRESHOLD_PARAMETER.data_type)]

    @overrides(AbstractThresholdType.get_threshold_parameter_types)
    def get_threshold_parameter_types(self):
        # TODO: update to return the parameter types
        return [item.data_type for item in _MY_THRESHOLD_TYPES]

    @overrides(AbstractThresholdType.get_n_cpu_cycles_per_neuron)
    def get_n_cpu_cycles_per_neuron(self):
        # TODO: update to the number of cycles used by\
        # threshold_type_is_above_threshold
        # Note: This can be guessed
        return 10
