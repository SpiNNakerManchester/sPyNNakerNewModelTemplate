from spynnaker.pyNN.models.neuron.input_types.abstract_input_type \
    import AbstractInputType
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter

from data_specification.enums.data_type import DataType

from enum import Enum


class _MY_INPUT_TYPES(Enum):

    MY_MULTIPLICATOR = (1, DataType.S1615)
    MY_INPUT_PARAMETER = (2, DataType.S1615)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


class MyInputType(AbstractInputType):

    def __init__(
            self, n_neurons,

            # TODO: update the parameters
            my_multiplicator,
            my_input_parameter):

        AbstractInputType.__init__(self)
        self._n_neurons = n_neurons

        # TODO: store the parameters
        self._my_multiplicator = \
            utility_calls.convert_param_to_numpy(
                my_multiplicator, n_neurons)
        self._my_input_parameter = \
            utility_calls.convert_param_to_numpy(
                my_input_parameter, n_neurons)

    # TODO: Add getters and setters for the parameters

    @property
    def my_multiplicator(self):
        return self._my_multiplicator

    @property
    def my_input_parameter(self):
        return self._my_input_parameter

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self._my_multiplicator = \
            utility_calls.convert_param_to_numpy(
                my_multiplicator, self._n_neurons)

    @my_input_parameter.setter
    def my_input_parameter(self, my_input_parameter):
        self._my_input_parameter = \
            utility_calls.convert_param_to_numpy(
                my_input_parameter, self._n_neurons)

    def get_global_weight_scale(self):
        return 1.0

    def get_n_input_type_parameters(self):
        """ Get the number of parameters for the input type

        :return: The number of parameters
        :rtype: int
        """
        # TODO: update the number of parameters this input type holds
        # Note: must match the number in the input_type_t structure
        # in the C code
        return 2

    def get_input_type_parameters(self):
        """ Get the parameters for the input type

        :return: An array of parameters
        :rtype: array of\
                :py:class:`spynnaker.pyNN.models.neural_properties.neural_parameter.NeuronParameter`
        """
        # TODO: update the parameters
        # Note: must match the order of the input_type_t structure in
        # the C code
        return [
            NeuronParameter(
                self._my_multiplicator,
                _MY_INPUT_TYPES.
                MY_MULTIPLICATOR.data_type),
            NeuronParameter(
                self._my_input_parameter,
                _MY_INPUT_TYPES.
                MY_INPUT_PARAMETER.data_type)
        ]

    def get_input_type_parameter_types(self):
        """ Get the parameter types for the input type

        :return: An array of parameter types
        """
        # TODO: update the parameter types
        return [item.data_type for item in _MY_INPUT_TYPES]

    def get_n_cpu_cycles_per_neuron(self, n_synapse_types):
        """ Get the number of CPU cycles executed in here... ?
        """
        # TODO: update to reflect the C code
        # Note: can be guessed to some extent
        return 0
