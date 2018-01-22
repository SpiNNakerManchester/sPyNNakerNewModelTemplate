# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex as Vertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp \
    import MyModelCurrExpBase as MyCurrExp


class MyModelCurrExpDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=Vertex.none_pynn_default_parameters[
                'spikes_per_second'],
            ring_buffer_sigma=Vertex.none_pynn_default_parameters[
                'ring_buffer_sigma'],
            incoming_spike_buffer_size=Vertex.none_pynn_default_parameters[
                'incoming_spike_buffer_size'],
            constraints=Vertex.none_pynn_default_parameters['constraints'],
            label=Vertex.none_pynn_default_parameters['label'],
            v_init=MyCurrExp.non_pynn_default_parameters['v_init'],
            v_thresh=MyCurrExp.default_parameters['v_thresh'],
            tau_syn_E=MyCurrExp.default_parameters['tau_syn_E'],
            tau_syn_I=MyCurrExp.default_parameters['tau_syn_I'],
            isyn_exc=MyCurrExp.default_parameters['isyn_exc'],
            isyn_inh=MyCurrExp.default_parameters['isyn_inh'],
            my_parameter=MyCurrExp.default_parameters['my_parameter'],
            i_offset=MyCurrExp.default_parameters['i_offset']):
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
        return MyCurrExp
