from spinn_utilities.overrides import overrides
from pacman.executor.injection_decorator import inject_items
from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spynnaker.pyNN.models.neuron.synapse_types import AbstractSynapseType
from spynnaker.pyNN.models.neural_properties import NeuronParameter
from spynnaker.pyNN.utilities.ranged.spynakker_ranged_dict import \
    SpynakkerRangeDictionary

from data_specification.enums import DataType

import numpy
from enum import Enum

# TODO create constants to EXACTLY match the parameter names
EX_SYNAPSE_NAME = 'my_ex_synapse_parameter'
IN_SYNAPE_NAME = 'my_in_synapse_parameter'
EXC_INIT_NAME = 'my_exc_init'
INH_INIT_NAME = 'my_inh_init'


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
    """ Convert a numpy array of tau into the decay constants required by the\
    SpiNNaker machine's fixed-point math. ::

        decay = numpy.exp(numpy.divide(-float(machine_time_step),
                                       numpy.multiply(1000.0, tau)))
        decay = numpy.exp(-float(machine_time_step)/ (1000.0 * tau)))
        init = numpy.multiply(numpy.multiply(tau, numpy.subtract(1.0, decay)),
                              (1000.0 / float(machine_time_step)))
        scale = float(pow(2, 32))
        decay_scaled = numpy.multiply(decay, scale).astype("uint32")
        init_scaled = numpy.multiply(init, scale).astype("uint32")

    :param tau: the decay time constants
    :type tau: numpy array
    :param machine_time_step: the machine time step factor
    """
    return tau.apply_operation(
        lambda x: int(numpy.exp(-float(machine_time_step)/(1000.0 * x)) *
                      pow(2, 32))), \
        tau.apply_operation(
            lambda x: int(x * (1.0 - numpy.exp(
                -float(machine_time_step)/(1000.0 * x))) *
                          (1000.0 / float(machine_time_step)) * pow(2, 32)))


class MySynapseType(AbstractSynapseType, AbstractContainsUnits):
    def __init__(
            self, n_neurons,

             # TODO: update the parameters
             my_ex_synapse_parameter=0.1,
             my_in_synapse_parameter=0.1,
             my_exc_init=0.0,
             my_inh_init=0.0):
        self._units = {
            EX_SYNAPSE_NAME: "mV",
            IN_SYNAPE_NAME: 'mV',
            EXC_INIT_NAME: "uS",
            INH_INIT_NAME: "uS"}

        self._n_neurons = n_neurons
        self._data = SpynakkerRangeDictionary(size=n_neurons)

        # TODO: Store the parameters
        self._data[EX_SYNAPSE_NAME] = my_ex_synapse_parameter
        self._data[IN_SYNAPE_NAME] = my_in_synapse_parameter
        self._data[EXC_INIT_NAME] = my_exc_init
        self._data[INH_INIT_NAME] = my_inh_init

    # TODO: Add any getters and setters for new parameters

    @property
    def my_ex_synapse_parameter(self):
        return self._data[EX_SYNAPSE_NAME]

    @my_ex_synapse_parameter.setter
    def my_ex_synapse_parameter(self, my_ex_synapse_parameter):
        self._data.set_value(
            key=EX_SYNAPSE_NAME, value=my_ex_synapse_parameter)

    @property
    def my_in_synapse_parameter(self):
        return self._data[IN_SYNAPE_NAME]

    @my_in_synapse_parameter.setter
    def my_in_synapse_parameter(self, my_in_synapse_parameter):
        self._data.set_value(
            key=IN_SYNAPE_NAME, value=my_in_synapse_parameter)

    @property
    def my_exc_init(self):
        return self._data[EXC_INIT_NAME]

    @my_exc_init.setter
    def my_exc_init(self, my_exc_init):
        self._data.set_value(key=EXC_INIT_NAME, value=my_exc_init)

    @property
    def my_inh_init(self):
        return self._data[INH_INIT_NAME]

    @my_inh_init.setter
    def my_inh_init(self, my_inh_init):
        self._data.set_value(key=INH_INIT_NAME, value=my_inh_init)

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
            self._data[EX_SYNAPSE_NAME], machine_time_step)
        i_decay, i_init = get_exponential_decay_and_init(
            self._data[IN_SYNAPE_NAME], machine_time_step)

        # TODO: update to return the parameters
        # Note: The order of the parameters must match the order in the
        # synapse_param_t data structure in the C code
        return [
            NeuronParameter(e_decay, _MY_SYNAPSE_TYPES.E_DECAY.data_type),
            NeuronParameter(e_init, _MY_SYNAPSE_TYPES.E_INIT.data_type),
            NeuronParameter(i_decay, _MY_SYNAPSE_TYPES.I_DECAY.data_type),
            NeuronParameter(i_init, _MY_SYNAPSE_TYPES.I_INIT.data_type),
            NeuronParameter(self._data[EXC_INIT_NAME],
                            _MY_SYNAPSE_TYPES.INITIAL_EXC.data_type),
            NeuronParameter(self._data[INH_INIT_NAME],
                            _MY_SYNAPSE_TYPES.INITIAL_INH.data_type)]

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
