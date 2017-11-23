from pacman.executor.injection_decorator import inject_items
from pacman.model.decorators.overrides import overrides
from spinn_utilities.ranged.range_dictionary import RangeDictionary
from spynnaker.pyNN.models.neural_properties import NeuronParameter
from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spynnaker.pyNN.models.neuron.neuron_models import AbstractNeuronModel
from data_specification.enums import DataType

from enum import Enum

# TODO create constants to EXACTLY match the parameter names
I_OFFSET_NAME = "i_offset"
MY_PARAMETER_NAME = "my_parameter_1"
V_INIT_NAME = "v_init"


class _MY_NEURON_MODEL_TYPES(Enum):

    V_INIT = (1, DataType.S1615)
    I_OFFSET = (2, DataType.S1615)
    MY_NEURON_PARAMETER = (3, DataType.S1615)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


class MyNeuronModel(AbstractNeuronModel, AbstractContainsUnits):

    def __init__(
            self, n_neurons,

            # TODO: update the parameters
            i_offset, my_neuron_parameter,

            # TODO: update the state variables if required
            v_init=-70.0):
        AbstractNeuronModel.__init__(self)
        AbstractContainsUnits.__init__(self)

        self._units = {
            V_INIT_NAME: 'mV',
            MY_PARAMETER_NAME: 'mV',
            I_OFFSET_NAME: 'nA'}

        self._n_neurons = n_neurons

        self._data = RangeDictionary(size=n_neurons)

        # TODO: Store any parameters
        self._data[I_OFFSET_NAME] = i_offset
        self._data[MY_PARAMETER_NAME] = my_neuron_parameter

        # TODO: Store any state variables
        self._data[V_INIT_NAME] = v_init

    # TODO: Add getters and setters for the parameters

    @property
    def i_offset(self):
        return self._data[I_OFFSET_NAME]

    @i_offset.setter
    def i_offset(self, i_offset):
        self._data.set_value(key=I_OFFSET_NAME, value=i_offset)

    @property
    def my_neuron_parameter(self):
        return self._data[MY_PARAMETER_NAME]

    @my_neuron_parameter.setter
    def my_neuron_parameter(self, my_neuron_parameter):
        self._data.set_value(
            key=MY_PARAMETER_NAME, value=my_neuron_parameter)

    # TODO: Add initialisers for the state variables

    def initialize_v(self, v_init):
        self._data.set_value(key=V_INIT_NAME, value=v_init)

    def get_n_neural_parameters(self):

        # TODO: update to match the number of parameters
        # Note: this must match the number of parameters in the neuron_t
        # data structure in the C code
        return 3

    def get_neural_parameters(self):

        # TODO: update to match the parameters and state variables
        # Note: this must match the order of the parameters in the neuron_t
        # data structure in the C code
        return [

            # REAL V;
            NeuronParameter(self._data[V_INIT_NAME],
                            _MY_NEURON_MODEL_TYPES.V_INIT.data_type),

            # REAL I_offset;
            NeuronParameter(self._data[I_OFFSET_NAME],
                            _MY_NEURON_MODEL_TYPES.I_OFFSET.data_type),

            # REAL my_parameter;
            NeuronParameter(self._data[MY_PARAMETER_NAME],
                            _MY_NEURON_MODEL_TYPES.
                            MY_NEURON_PARAMETER.data_type)
        ]

    def get_neural_parameter_types(self):

        # TODO: update to match the parameter types
        return [item.data_type for item in _MY_NEURON_MODEL_TYPES]

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
        return 80

    @overrides(AbstractContainsUnits.get_units)
    def get_units(self, variable):
        return self._units[variable]
