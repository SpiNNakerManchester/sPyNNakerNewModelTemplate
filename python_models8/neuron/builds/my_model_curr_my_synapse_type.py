# main interface to use the spynnaker related tools.
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic

from python_models8.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel
from python_models8.neuron.synapse_types.my_synapse_type \
    import MySynapseType

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class MyModelCurrMySynapseTypeBase(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = 256

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'v_thresh': -50.0, 'my_ex_synapse_parameter': 0.1,
        'my_in_synapse_parameter': 0.1,
        'i_offset': 0, 'my_parameter': -70.0,
        'my_exc_init': 0.0, 'my_inh_init': 0.0}

    initialize_parameters = {'v_init': None}

    def __init__(
            self, n_neurons,
            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs['incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],


            # neuron model parameters
            my_parameter=default_parameters['my_parameter'],
            i_offset=default_parameters['i_offset'],

            # threshold types parameters
            v_thresh=default_parameters['v_thresh'],

            # synapse type parameters
            my_ex_synapse_parameter=default_parameters[
                'my_ex_synapse_parameter'],
            my_in_synapse_parameter=default_parameters[
                'my_in_synapse_parameter'],
            my_exc_init=default_parameters[
                'my_exc_init'],
            my_inh_init=default_parameters[
                'my_inh_init'],

            # state variables
            v_init=initialize_parameters['v_init']):

        # create neuron model class
        neuron_model = MyNeuronModel(
            n_neurons, i_offset, my_parameter)

        # create synapse type model
        synapse_type = MySynapseType(
            n_neurons, my_ex_synapse_parameter,
            my_in_synapse_parameter, my_exc_init, my_inh_init)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = ThresholdTypeStatic(n_neurons, v_thresh)

        # create additional inputs
        additional_input = None

        # instantiate the sPyNNaker system by initialising
        # the AbstractPopulationVertex
        super(MyModelCurrMySynapseTypeBase, self).__init__(
            # standard inputs, do not need to change.
            n_neurons=n_neurons, label=label, constraints=constraints,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,

            max_atoms_per_core=(
                MyModelCurrMySynapseTypeBase._model_based_max_atoms_per_core),

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input=additional_input,

            # the model a name (shown in reports)
            model_name="MyModelMySynapseType",

            # the matching binary name
            binary="my_model_curr_my_synapse_type.aplx")

    @staticmethod
    def get_max_atoms_per_core():

        return MyModelCurrMySynapseTypeBase._model_based_max_atoms_per_core

    @staticmethod
    def set_max_atoms_per_core(new_value):

        MyModelCurrMySynapseTypeBase._model_based_max_atoms_per_core = \
            new_value

    @property
    def my_parameter(self):
        return self.default_parameters['my_parameter']

    @property
    def my_ex_synapse_parameter(self):
        return self.default_parameters['my_ex_synapse_parameter']

    @property
    def my_in_synapse_parameter(self):
        return self.default_parameters['my_in_synapse_parameter']

    @property
    def my_exc_init(self):
        return self.default_parameters['my_exc_init']

    @property
    def my_inh_init(self):
        return self.default_parameters['my_inh_init']
