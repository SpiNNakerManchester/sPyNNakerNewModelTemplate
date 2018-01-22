# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex as Vertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp_my_threshold \
    import MyModelCurrExpMyThresholdBase as MyThreshold


class MyModelCurrExpMyThresholdDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=Vertex.none_pynn_default_parameters[
                'spikes_per_second'],
            ring_buffer_sigma=Vertex.none_pynn_default_parameters[
                'ring_buffer_sigma'],
            incoming_spike_buffer_size=Vertex.none_pynn_default_parameters[
                'incoming_spike_buffer_size'],
            constraints=Vertex.none_pynn_default_parameters['constraints'],
            label=Vertex.none_pynn_default_parameters['label'],
            v_init=MyThreshold.non_pynn_default_parameters['v_init'],
            tau_syn_E=MyThreshold.default_parameters['tau_syn_E'],
            tau_syn_I=MyThreshold.default_parameters['tau_syn_I'],
            isyn_exc=MyThreshold.default_parameters['isyn_exc'],
            isyn_inh=MyThreshold.default_parameters['isyn_inh'],
            my_threshold_parameter=MyThreshold.default_parameters[
                'my_threshold_parameter'],
            threshold_value=MyThreshold.default_parameters['threshold_value'],
            my_parameter=MyThreshold.default_parameters['my_parameter'],
            i_offset=MyThreshold.default_parameters['i_offset']):
        super(MyModelCurrExpMyThresholdDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
            'i_offset': i_offset,
            'my_parameter': my_parameter,
            'my_threshold_parameter': my_threshold_parameter,
            'threshold_value': threshold_value,
            'v_init': v_init})

    @staticmethod
    def build_model():
        return MyThreshold
