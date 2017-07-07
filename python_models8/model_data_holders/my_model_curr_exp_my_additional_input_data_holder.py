# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp_my_additional_input \
    import MyModelCurrExpMyAdditionalInputBase


class MyModelCurrExpMyAdditionalInputDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=(
                AbstractPopulationVertex.none_pynn_default_parameters[
                    'spikes_per_second']),
            ring_buffer_sigma=(
                AbstractPopulationVertex.none_pynn_default_parameters[
                    'ring_buffer_sigma']),
            incoming_spike_buffer_size=(
                AbstractPopulationVertex.none_pynn_default_parameters[
                    'incoming_spike_buffer_size']),
            constraints=AbstractPopulationVertex.none_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.none_pynn_default_parameters[
                'label'],
            v_init=(
                MyModelCurrExpMyAdditionalInputBase
                .none_pynn_default_parameters['v_init']),
            v_thresh=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'v_thresh'],
            tau_syn_E=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'tau_syn_E'],
            tau_syn_I=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'tau_syn_I'],
            isyn_exc=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'isyn_exc'],
            isyn_inh=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'isyn_inh'],
            my_additional_input_parameter=(
                MyModelCurrExpMyAdditionalInputBase.default_parameters[
                    'my_additional_input_parameter']),
            my_parameter=(
                MyModelCurrExpMyAdditionalInputBase.default_parameters[
                    'my_parameter']),
            i_offset=MyModelCurrExpMyAdditionalInputBase.default_parameters[
                'i_offset']):
        DataHolder.__init__(
            self, {
                'spikes_per_second': spikes_per_second,
                'ring_buffer_sigma': ring_buffer_sigma,
                'incoming_spike_buffer_size': incoming_spike_buffer_size,
                'constraints': constraints,
                'label': label,
                'v_thresh': v_thresh,
                'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
                'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
                'i_offset': i_offset,
                'my_parameter': my_parameter,
                'my_additional_input_parameter': my_additional_input_parameter,
                'v_init': v_init})

    @staticmethod
    def build_model():
        return MyModelCurrExpMyAdditionalInputBase
