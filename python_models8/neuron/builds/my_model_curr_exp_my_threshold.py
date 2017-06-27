# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential

from python_models8.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel
from python_models8.neuron.threshold_types.my_threshold_type \
    import MyThresholdType


class MyModelCurrExpMyThresholdBase(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = 256

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
        'isyn_exc': 0.0, 'isyn_inh': 0.0,
        'i_offset': 0, 'my_parameter': -70.0,
        'my_threshold_parameter': 0.5,
        'threshold_value': -10.0}

    none_pynn_default_parameters = {'v_init': None}

    def __init__(
            self, n_neurons, spikes_per_second=AbstractPopulationVertex.
            none_pynn_default_parameters['spikes_per_second'],
            ring_buffer_sigma=AbstractPopulationVertex.
            none_pynn_default_parameters['ring_buffer_sigma'],
            incoming_spike_buffer_size=AbstractPopulationVertex.
            none_pynn_default_parameters['incoming_spike_buffer_size'],
            constraints=AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],

            # neuron model parameters
            my_parameter=default_parameters['my_parameter'],
            i_offset=default_parameters['i_offset'],

            # threshold types parameters
            my_threshold_parameter=(
                default_parameters['my_threshold_parameter']),
            threshold_value=default_parameters['threshold_value'],

            # synapse type parameters
            tau_syn_E=default_parameters['tau_syn_E'],
            tau_syn_I=default_parameters['tau_syn_I'],
            isyn_exc=default_parameters['isyn_exc'],
            isyn_inh=default_parameters['isyn_inh'],

            # state variables
            v_init=None):

        # create neuron model class
        neuron_model = MyNeuronModel(
            n_neurons, i_offset, my_parameter)

        # create synapse type model
        synapse_type = SynapseTypeExponential(
            n_neurons, tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = MyThresholdType(
            n_neurons, threshold_value, my_threshold_parameter)

        # create additional inputs
        additional_input = None

        # instantiate the sPyNNaker system by initialising
        #  the AbstractPopulationVertex
        AbstractPopulationVertex.__init__(

            # standard inputs, do not need to change.
            self, n_neurons=n_neurons, label=label,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,

            max_atoms_per_core=(
                MyModelCurrExpMyThresholdBase._model_based_max_atoms_per_core),

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input=additional_input,

            # the model a name (shown in reports)
            model_name="MyModelCurrExpMyThreshold",

            # the matching binary name
            binary="my_model_curr_exp_my_threshold.aplx")

    @staticmethod
    def get_max_atoms_per_core():

        return MyModelCurrExpMyThresholdBase._model_based_max_atoms_per_core

    @staticmethod
    def set_max_atoms_per_core(new_value):
        MyModelCurrExpMyThresholdBase._model_based_max_atoms_per_core = \
            new_value

    @property
    def my_threshold_parameter(self):
        return self.default_parameters['my_threshold_parameter']

    @property
    def threshold_value(self):
        return self.default_parameters['threshold_value']

    @property
    def my_parameter(self):
        return self.default_parameters['my_parameter']
