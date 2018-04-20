# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp import MyModelCurrExpBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class MyModelCurrExpDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs['incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],
            v_init=MyModelCurrExpBase.initialize_parameters['v_init'],
            v_thresh=MyModelCurrExpBase.default_parameters['v_thresh'],
            tau_syn_E=MyModelCurrExpBase.default_parameters['tau_syn_E'],
            tau_syn_I=MyModelCurrExpBase.default_parameters['tau_syn_I'],
            isyn_exc=MyModelCurrExpBase.default_parameters['isyn_exc'],
            isyn_inh=MyModelCurrExpBase.default_parameters['isyn_inh'],
            my_parameter=MyModelCurrExpBase.default_parameters['my_parameter'],
            i_offset=MyModelCurrExpBase.default_parameters['i_offset']):
        super(MyModelCurrExpDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'v_thresh': v_thresh,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
            'i_offset': i_offset,
            'my_parameter': my_parameter, 'v_init': v_init})

    @staticmethod
    def build_model():
        return MyModelCurrExpBase
