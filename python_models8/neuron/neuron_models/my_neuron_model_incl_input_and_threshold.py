from pacman.executor.injection_decorator import inject_items
from pacman.model.decorators.overrides import overrides
from spynnaker.pyNN.models.neural_properties import NeuronParameter
from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spynnaker.pyNN.models.neuron.neuron_models import AbstractNeuronModel
from spynnaker.pyNN.utilities import utility_calls
from data_specification.enums import DataType

from enum import Enum


class _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES(Enum):

    V_INIT = (1, DataType.S1615)
    I_OFFSET = (2, DataType.S1615)
    MY_NEURON_PARAMETER = (3, DataType.S1615)
    MY_MULTIPLICATOR = (4, DataType.S1615)
    MY_INPUT_PARAMETER = (5, DataType.S1615)
    THRESHOLD_VALUE = (6, DataType.S1615)
    MY_THRESHOLD_PARAMETER = (7, DataType.S1615)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


class MyNeuronModelInclInputAndThreshold(AbstractNeuronModel,
                                         AbstractContainsUnits):

    def __init__(
            self, n_neurons,

            # TODO: update the parameters
            i_offset, my_neuron_parameter,
            my_multiplicator, my_input_parameter,
            threshold_value, my_threshold_parameter,

            # TODO: update the state variables if required
            v_init=-70.0):
        AbstractNeuronModel.__init__(self)
        AbstractContainsUnits.__init__(self)

        self._units = {
            'v_init': 'mV',
            'my_neuron_parameter': 'mV',
            'v_thresh': 'mV',
            'my_multiplicator': '',
            'my_input_parmaeter': 'nA',
            'threshold_value': 'mV',
            'my_threshold_parameter': '',
            'i_offset': 'nA'}

        self._n_neurons = n_neurons

        # TODO: Store any parameters
        self._i_offset = utility_calls.convert_param_to_numpy(
            i_offset, n_neurons)
        self._my_neuron_parameter = utility_calls.convert_param_to_numpy(
            my_neuron_parameter, n_neurons)
        self._my_multiplicator = utility_calls.convert_param_to_numpy(
            my_multiplicator, n_neurons)
        self._my_input_parameter = utility_calls.convert_param_to_numpy(
            my_input_parameter, n_neurons)
        self._threshold_value = utility_calls.convert_param_to_numpy(
            threshold_value, n_neurons)
        self._my_threshold_parameter = utility_calls.convert_param_to_numpy(
            my_threshold_parameter, n_neurons)

        # TODO: Store any state variables
        self._v_init = utility_calls.convert_param_to_numpy(v_init, n_neurons)

    # Need to define this function here now!
    def get_global_weight_scale(self):
        return 1.0

    # TODO: Add getters and setters for the parameters

    @property
    def i_offset(self):
        return self._i_offset

    @i_offset.setter
    def i_offset(self, i_offset):
        self._i_offset = utility_calls.convert_param_to_numpy(
            i_offset, self._n_neurons)

    @property
    def my_neuron_parameter(self):
        return self._my_neuron_parameter

    @my_neuron_parameter.setter
    def my_neuron_parameter(self, my_neuron_parameter):
        self._my_neuron_parameter = utility_calls.convert_param_to_numpy(
            my_neuron_parameter, self._n_neurons)

    @property
    def my_multiplicator(self):
        return self._my_multiplicator

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self._my_multiplicator = utility_calls.convert_param_to_numpy(
            my_multiplicator, self._n_neurons)

    @property
    def my_input_parameter(self):
        return self._my_input_parameter

    @my_input_parameter.setter
    def my_input_parameter(self, my_input_parameter):
        self._my_input_parameter = utility_calls.convert_param_to_numpy(
            my_input_parameter, self._n_neurons)

    @property
    def threshold_value(self):
        return self._threshold_value

    @threshold_value.setter
    def threshold_value(self, threshold_value):
        self._threshold_value = utility_calls.convert_param_to_numpy(
            threshold_value, self._n_neurons)

    @property
    def my_threshold_parameter(self):
        return self._my_threshold_parameter

    @my_threshold_parameter.setter
    def my_threshold_parameter(self, my_threshold_parameter):
        self._my_threshold_parameter = utility_calls.convert_param_to_numpy(
            my_threshold_parameter, self._n_neurons)

    # TODO: Add initialisers for the state variables

    def initialize_v(self, v_init):
        self._v_init = utility_calls.convert_param_to_numpy(
            v_init, self._n_neurons)

    def get_n_neural_parameters(self):

        # TODO: update to match the number of parameters
        # Note: this must match the number of parameters in the neuron_t
        # data structure in the C code
        return 7

    def get_neural_parameters(self):

        # TODO: update to match the parameters and state variables
        # Note: this must match the order of the parameters in the neuron_t
        # data structure in the C code
        return [

            # REAL V;
            NeuronParameter(self._v_init,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            V_INIT.data_type),

            # REAL I_offset;
            NeuronParameter(self._i_offset,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            I_OFFSET.data_type),

            # REAL my_parameter;
            NeuronParameter(self._my_neuron_parameter,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_NEURON_PARAMETER.data_type),

            # REAL my_multiplicator;
            NeuronParameter(self._my_multiplicator,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_MULTIPLICATOR.data_type),

            # REAL my_input_parameter;
            NeuronParameter(self._my_input_parameter,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_INPUT_PARAMETER.data_type),

            # REAL threshold_value;
            NeuronParameter(self._threshold_value,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            THRESHOLD_VALUE.data_type),

            # REAL my_threshold_parameter;
            NeuronParameter(self._my_threshold_parameter,
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_THRESHOLD_PARAMETER.data_type)

        ]

    def get_neural_parameter_types(self):

        # TODO: update to match the parameter types
        return [item.data_type
                for item in _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES]

    def get_n_global_parameters(self):

        # TODO: update to match the number of global parameters
        # Note: This must match the number of parameters in the global_neuron_t
        # data structure in the C code
        return 1

    @inject_items({"machine_time_step": "MachineTimeStep"})
    def get_global_parameters(self, machine_time_step):

        # TODO: update to match the global parameters
        # Note: This must match the order of the parameters in the
        # global_neuron_t data structure in the C code
        return [
            # uint32_t machine_time_step
            NeuronParameter(machine_time_step, DataType.UINT32)
        ]

    def get_global_parameter_types(self):

        # TODO update to match the global parameter type
        return [DataType.UINT32]

    def get_n_cpu_cycles_per_neuron(self):

        # TODO: update with the number of CPU cycles taken by the
        # neuron_model_state_update, neuron_model_get_membrane_voltage
        # and neuron_model_has_spiked functions in the C code
        # Note: This can be a guess
        return 100

    @overrides(AbstractContainsUnits.get_units)
    def get_units(self, variable):
        return self._units[variable]
