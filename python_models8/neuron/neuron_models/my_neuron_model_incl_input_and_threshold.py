from pacman.executor.injection_decorator import inject_items
from pacman.model.decorators.overrides import overrides
from spynnaker.pyNN.models.neural_properties import NeuronParameter
from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spynnaker.pyNN.models.neuron.neuron_models import AbstractNeuronModel
from spynnaker.pyNN.utilities.ranged.spynakker_ranged_dict import \
    SpynakkerRangeDictionary
from data_specification.enums import DataType

from enum import Enum

# TODO create constants to EXACTLY match the parameter names
I_OFFSET_NAME = "i_offset"
MY_NEURON_PARAMETER_NAME = "my_neuron_parameter"
V_INIT_NAME = "v_init"
MY_MULTIPLICATOR_NAME = "my_multiplicator"
MY_INPUT_PARAMETER_NAME = "my_input_parameter"
THRESHOLD_VALUE_NAME = "threshold_value"
MY_THRESHOLD_PARAMETER_NAME = "my_threshold_parameter"


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

        self._units = {
            'v_init': 'mV',
            'my_neuron_parameter': 'mV',
            'my_multiplicator': '',
            'my_input_parmaeter': 'nA',
            'threshold_value': 'mV',
            'my_threshold_parameter': '',
            'i_offset': 'nA'}

        self._n_neurons = n_neurons

        self._data = SpynakkerRangeDictionary(size=n_neurons)

        # TODO: Store any parameters
        self._data[I_OFFSET_NAME] = i_offset
        self._data[MY_NEURON_PARAMETER_NAME] = my_neuron_parameter
        self._data[MY_MULTIPLICATOR_NAME] = my_multiplicator
        self._data[MY_INPUT_PARAMETER_NAME] = my_input_parameter
        self._data[THRESHOLD_VALUE_NAME] = threshold_value
        self._data[MY_THRESHOLD_PARAMETER_NAME] = my_threshold_parameter

        # TODO: Store any state variables
        self._data[V_INIT_NAME] = v_init

    # Need to define this function here for this model!
    def get_global_weight_scale(self):
        return 1.0

    # TODO: Add getters and setters for the parameters

    @property
    def i_offset(self):
        return self._data[I_OFFSET_NAME]

    @i_offset.setter
    def i_offset(self, i_offset):
        self._data.set_value(key=I_OFFSET_NAME, value=i_offset)

    @property
    def my_neuron_parameter(self):
        return self._data[MY_NEURON_PARAMETER_NAME]

    @my_neuron_parameter.setter
    def my_neuron_parameter(self, my_neuron_parameter):
        self._data.set_value(key=MY_NEURON_PARAMETER_NAME,
                             value=my_neuron_parameter)

    @property
    def my_multiplicator(self):
        return self._data[MY_MULTIPLICATOR_NAME]

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self._data.set_value(key=MY_MULTIPLICATOR_NAME,
                             value=my_multiplicator)

    @property
    def my_input_parameter(self):
        return self._data[MY_INPUT_PARAMETER_NAME]

    @my_input_parameter.setter
    def my_input_parameter(self, my_input_parameter):
        self._data.set_value(key=MY_INPUT_PARAMETER_NAME,
                             value=my_input_parameter)

    @property
    def threshold_value(self):
        return self._data[THRESHOLD_VALUE_NAME]

    @threshold_value.setter
    def threshold_value(self, threshold_value):
        self._data.set_value(key=THRESHOLD_VALUE_NAME, value=threshold_value)

    @property
    def my_threshold_parameter(self):
        return self._data[MY_THRESHOLD_PARAMETER_NAME]

    @my_threshold_parameter.setter
    def my_threshold_parameter(self, my_threshold_parameter):
        self._data.set_value(key=MY_THRESHOLD_PARAMETER_NAME,
                             value=my_threshold_parameter)

    # TODO: Add initialisers for the state variables

    def initialize_v(self, v_init):
        self._data.set_value(key=V_INIT_NAME, value=v_init)

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
            NeuronParameter(self._data[V_INIT_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            V_INIT.data_type),

            # REAL I_offset;
            NeuronParameter(self._data[I_OFFSET_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            I_OFFSET.data_type),

            # REAL my_parameter;
            NeuronParameter(self._data[MY_NEURON_PARAMETER_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_NEURON_PARAMETER.data_type),

            # REAL my_multiplicator;
            NeuronParameter(self._data[MY_MULTIPLICATOR_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_MULTIPLICATOR.data_type),

            # REAL my_input_parameter;
            NeuronParameter(self._data[MY_INPUT_PARAMETER_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            MY_INPUT_PARAMETER.data_type),

            # REAL threshold_value;
            NeuronParameter(self._data[THRESHOLD_VALUE_NAME],
                            _MY_NEURON_MODEL_INCL_INPUT_AND_THRESHOLD_TYPES.
                            THRESHOLD_VALUE.data_type),

            # REAL my_threshold_parameter;
            NeuronParameter(self._data[MY_THRESHOLD_PARAMETER_NAME],
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
