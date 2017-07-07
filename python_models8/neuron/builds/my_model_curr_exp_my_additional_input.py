# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic

from python_models8.neuron.additional_inputs.my_additional_input \
    import MyAdditionalInput
from python_models8.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel


class MyModelCurrExpMyAdditionalInputBase(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = 256

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'v_thresh': -50.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
        'isyn_exc': 0.0, 'isyn_inh': 0.0,
        'i_offset': 0, 'my_parameter': -70.0,
        'my_additional_input_parameter': 1.0}

    none_pynn_default_parameters = {'v_init': None}

    def __init__(
            self, n_neurons, spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None, constraints=None, label=None,

            # neuron model parameters
            my_parameter=default_parameters['my_parameter'],
            i_offset=default_parameters['i_offset'],

            # threshold types parameters
            v_thresh=default_parameters['v_thresh'],

            # synapse type parameters
            tau_syn_E=default_parameters['tau_syn_E'],
            tau_syn_I=default_parameters['tau_syn_I'],
            isyn_exc=default_parameters['isyn_exc'],
            isyn_inh=default_parameters['isyn_inh'],

            # additional input parameter
            my_additional_input_parameter=(
                default_parameters['my_additional_input_parameter']),

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
        threshold_type = ThresholdTypeStatic(
            n_neurons, v_thresh)

        # create additional inputs
        additional_input = MyAdditionalInput(
            n_neurons, my_additional_input_parameter)

        # instantiate the sPyNNaker system by initialising
        #  the AbstractPopulationVertex
        AbstractPopulationVertex.__init__(

            # standard inputs, do not need to change.
            self, n_neurons=n_neurons, label=label,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,

            max_atoms_per_core=(
                MyModelCurrExpMyAdditionalInputBase.
                _model_based_max_atoms_per_core),

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input=additional_input,

            # the model a name (shown in reports)
            model_name="MyModelCurrExpMyAdditionalInput",

            # the matching binary name
            binary="my_model_curr_exp_my_additional_input.aplx")

    @staticmethod
    def get_max_atoms_per_core():

        return (
            MyModelCurrExpMyAdditionalInputBase._model_based_max_atoms_per_core
        )

    @staticmethod
    def set_max_atoms_per_core(new_value):

        MyModelCurrExpMyAdditionalInputBase._model_based_max_atoms_per_core = \
            new_value

    @property
    def my_additional_input_parameter(self):
        return self.default_parameters['my_additional_input_parameter']

    @property
    def my_parameter(self):
        return self.default_parameters['my_parameter']
