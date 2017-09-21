from spinn_utilities.overrides import overrides

from pacman.executor.injection_decorator import inject_items

from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spynnaker.pyNN.models.neuron.synapse_types import AbstractSynapseType
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.models.neural_properties import NeuronParameter

from data_specification.enums import DataType

import numpy
from enum import Enum


class _MY_SYNAPSE_TYPES(Enum):

    E_DECAY = (1, DataType.UINT32)
    E_INIT = (2, DataType.UINT32)
    I_DECAY = (3, DataType.UINT32)
    I_INIT = (4, DataType.UINT32)
    INITIAL_EXC = (5, DataType.S1615)
    INITIAL_INH = (6, DataType.S1615)

    def __new__(cls, value, data_type):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        return obj

    @property
    def data_type(self):
        return self._data_type


def get_exponential_decay_and_init(tau, machine_time_step):
    decay = numpy.exp(numpy.divide(-float(machine_time_step),
                                   numpy.multiply(1000.0, tau)))
    init = numpy.multiply(numpy.multiply(tau, numpy.subtract(1.0, decay)),
                          (1000.0 / float(machine_time_step)))
    scale = float(pow(2, 32))
    decay_scaled = numpy.multiply(decay, scale).astype("uint32")
    init_scaled = numpy.multiply(init, scale).astype("uint32")
    return decay_scaled, init_scaled


class MySynapseType(AbstractSynapseType, AbstractContainsUnits):

    def __init__(self, n_neurons,

                 # TODO: update the parameters
                 my_ex_synapse_parameter=0.1,
                 my_in_synapse_parameter=0.1,
                 my_exc_init=0.0,
                 my_inh_init=0.0):

        AbstractSynapseType.__init__(self)
        AbstractContainsUnits.__init__(self)

        self._units = {
            'my_ex_synapse_parameter': "mV",
            'my_in_synapse_parameter': 'mV',
            'my_exc_init': "uS",
            'my_inh_init': "uS"}

        self._n_neurons = n_neurons

        # TODO: Store the parameters
        self._my_ex_synapse_parameter = utility_calls.convert_param_to_numpy(
            my_ex_synapse_parameter, n_neurons)
        self._my_in_synapse_parameter = utility_calls.convert_param_to_numpy(
            my_in_synapse_parameter, n_neurons)
        self._my_exc_init = utility_calls.convert_param_to_numpy(
            my_exc_init, n_neurons)
        self._my_inh_init = utility_calls.convert_param_to_numpy(
            my_inh_init, n_neurons)

    # TODO: Add any getters and setters for new parameters

    @property
    def my_ex_synapse_parameter(self):
        return self._my_ex_synapse_parameter

    @my_ex_synapse_parameter.setter
    def my_ex_synapse_parameter(self, my_ex_synapse_parameter):
        self._my_ex_synapse_parameter = utility_calls.convert_param_to_numpy(
            my_ex_synapse_parameter, self._n_neurons)

    @property
    def my_in_synapse_parameter(self):
        return self._my_in_synapse_parameter

    @my_in_synapse_parameter.setter
    def my_in_synapse_parameter(self, my_in_synapse_parameter):
        self._my_in_synapse_parameter = utility_calls.convert_param_to_numpy(
            my_in_synapse_parameter, self._n_neurons)

    @property
    def my_exc_init(self):
        return self._my_exc_init

    @my_exc_init.setter
    def my_exc_init(self, my_exc_init):
        self._my_exc_init = utility_calls.convert_param_to_numpy(
            my_exc_init, self._n_neurons)

    @property
    def my_inh_init(self):
        return self._my_inh_init

    @my_inh_init.setter
    def my_inh_init(self, my_inh_init):
        self._my_inh_init = utility_calls.convert_param_to_numpy(
            my_inh_init, self._n_neurons)

    def get_n_synapse_types(self):

        # TODO: Update with the number of supported synapse types
        return 2

    def get_synapse_id_by_target(self, target):

        # TODO: update the mapping from name to id
        if target == "excitatory":
            return 0
        elif target == "inhibitory":
            return 1
        return None

    def get_synapse_targets(self):

        # TODO: update to return the same names as above
        return "excitatory", "inhibitory"

    def get_n_synapse_type_parameters(self):

        # TODO: Return the number of parameters
        # Note: This must match the number of parameters in the
        # synapse_param_t data structure in the C code
        return 6

    @inject_items({"machine_time_step": "MachineTimeStep"})
    def get_synapse_type_parameters(self, machine_time_step):

        e_decay, e_init = get_exponential_decay_and_init(
            self._my_ex_synapse_parameter, machine_time_step)
        i_decay, i_init = get_exponential_decay_and_init(
            self._my_in_synapse_parameter, machine_time_step)

        # TODO: update to return the parameters
        # Note: The order of the parameters must match the order in the
        # synapse_param_t data structure in the C code
        return [
            NeuronParameter(e_decay, _MY_SYNAPSE_TYPES.E_DECAY.data_type),
            NeuronParameter(e_init, _MY_SYNAPSE_TYPES.E_INIT.data_type),
            NeuronParameter(i_decay, _MY_SYNAPSE_TYPES.I_DECAY.data_type),
            NeuronParameter(i_init, _MY_SYNAPSE_TYPES.I_INIT.data_type),
            NeuronParameter(
                self._my_exc_init, _MY_SYNAPSE_TYPES.INITIAL_EXC.data_type),
            NeuronParameter(
                self._my_inh_init, _MY_SYNAPSE_TYPES.INITIAL_INH.data_type),
        ]

    def get_synapse_type_parameter_types(self):

        # TODO: update to return the parameter types
        return [item.data_type for item in _MY_SYNAPSE_TYPES]

    def get_n_cpu_cycles_per_neuron(self):

        # TODO: update to match the number of cycles used by
        # synapse_types_shape_input, synapse_types_add_neuron_input,
        # synapse_types_get_excitatory_input and
        # synapse_types_get_inhibitory_input
        return 100

    @overrides(AbstractContainsUnits.get_units)
    def get_units(self, variable):
        return self._units[variable]
