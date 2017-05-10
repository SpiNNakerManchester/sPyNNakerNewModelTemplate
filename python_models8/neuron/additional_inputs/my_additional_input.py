from spynnaker.pyNN.models.neuron.additional_inputs.abstract_additional_input \
    import AbstractAdditionalInput
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter

from data_specification.enums.data_type import DataType


class MyAdditionalInput(AbstractAdditionalInput):

    def __init__(
            self, n_neurons,

            # TODO: update the parameters
            my_additional_input_parameter):

        AbstractAdditionalInput.__init__(self)
        self._n_neurons = n_neurons

        # TODO: store the parameters
        self._my_additional_input_parameter = \
            utility_calls.convert_param_to_numpy(
                my_additional_input_parameter, n_neurons)

    # TODO: Add getters and setters for the parameters

    @property
    def my_additional_input_parameter(self):
        return self._my_parameter

    @my_additional_input_parameter.setter
    def my_additional_input_parameter(self, my_additional_input_parameter):
        self._my_additional_input_parameter = \
            utility_calls.convert_param_to_numpy(
                my_additional_input_parameter, self._n_neurons)

    def get_n_parameters(self):
        """ Get the number of parameters for the additional input

        :return: The number of parameters
        :rtype: int
        """
        # TODO: update the number of parameters this additional input holds
        # Note: must match the number in the additional_input_t structure
        # in the C code
        return 2

    def get_parameters(self):
        """ Get the parameters for the additional input

        :return: An array of parameters
        :rtype: array of\
                :py:class:`spynnaker.pyNN.models.neural_properties.neural_parameter.NeuronParameter`
        """
        # TODO: update the parameters
        # Note: must match the order of the additional_input_t structure in
        # the C code
        return [
            NeuronParameter(0, DataType.S1615),
            NeuronParameter(
                self._my_additional_input_parameter, DataType.S1615),
        ]

    def get_parameter_types(self):
        """ Get the parameter types for the additional input

        :return: An array of parameter types
        """
        #TODO: update the parameter types
        return [item.data_type for item in DataType]

    def get_n_cpu_cycles_per_neuron(self):
        """ Get the number of CPU cycles executed by\
            additional_input_get_input_value_as_current and\
            additional_input_has_spiked
        """
        # TODO: update to reflect the C code
        # Note: can be guessed to some extent
        return 10
