# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex as Vertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp_my_threshold \
    import MyModelCurrExpMyThresholdBase as MyThreshold

# Merge the defaults together
_defaults = dict(Vertex.none_pynn_default_parameters)
_defaults.update(MyThreshold.non_pynn_default_parameters)
_defaults.update(MyThreshold.default_parameters)


class MyModelCurrExpMyThresholdDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=_defaults['spikes_per_second'],
            ring_buffer_sigma=_defaults['ring_buffer_sigma'],
            incoming_spike_buffer_size=_defaults['incoming_spike_buffer_size'],
            constraints=_defaults['constraints'],
            label=_defaults['label'],
            v_init=_defaults['v_init'],
            tau_syn_E=_defaults['tau_syn_E'],
            tau_syn_I=_defaults['tau_syn_I'],
            isyn_exc=_defaults['isyn_exc'],
            isyn_inh=_defaults['isyn_inh'],
            my_threshold_parameter=_defaults['my_threshold_parameter'],
            threshold_value=_defaults['threshold_value'],
            my_parameter=_defaults['my_parameter'],
            i_offset=_defaults['i_offset']):
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
