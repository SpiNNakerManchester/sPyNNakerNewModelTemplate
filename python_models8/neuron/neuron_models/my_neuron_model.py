from pacman.executor.injection_decorator import inject_items
from pacman.model.decorators.overrides import overrides
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter
from spynnaker.pyNN.models.abstract_models.abstract_contains_units import \
    AbstractContainsUnits
from spynnaker.pyNN.models.neuron.neuron_models.abstract_neuron_model \
    import AbstractNeuronModel
from spynnaker.pyNN.utilities import utility_calls

from data_specification.enums.data_type import DataType


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
            'v_init': 'mV',
            'my_neuron_parameter': 'mV',
            'i_offset': 'nA'}

        self._n_neurons = n_neurons

        # TODO: Store any parameters
        self._i_offset = utility_calls.convert_param_to_numpy(
            i_offset, n_neurons)
        self._my_neuron_parameter = utility_calls.convert_param_to_numpy(
            my_neuron_parameter, n_neurons)

        # TODO: Store any state variables
        self._v_init = utility_calls.convert_param_to_numpy(v_init, n_neurons)

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

    # TODO: Add initialisers for the state variables

    def initialize_v(self, v_init):
        self._v_init = utility_calls.convert_param_to_numpy(
            v_init, self._n_neurons)

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
            NeuronParameter(self._v_init, DataType.S1615),

            # REAL I_offset;
            NeuronParameter(self._i_offset, DataType.S1615),

            # REAL my_parameter;
            NeuronParameter(self._my_neuron_parameter, DataType.S1615)
        ]

    def get_neural_parameter_types(self):

        # TODO: update to match the parameter types
        return [item.data_type for item in DataType]

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
