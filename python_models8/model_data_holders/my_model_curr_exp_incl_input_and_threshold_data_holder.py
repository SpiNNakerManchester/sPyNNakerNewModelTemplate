# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp_incl_input_and_threshold \
    import MyModelCurrExpInclInputAndThresholdBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters
_defaults = MyModelCurrExpInclInputAndThresholdBase.default_parameters
_inits = MyModelCurrExpInclInputAndThresholdBase.initialize_parameters


class MyModelCurrExpInclInputAndThresholdDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=(
                _apv_defs['incoming_spike_buffer_size']),
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],
            v_init=_inits['v_init'],
            threshold_value=_defaults['threshold_value'],
            my_threshold_parameter=_defaults['my_threshold_parameter'],
            my_multiplicator=_defaults['my_multiplicator'],
            my_input_parameter=_defaults['my_input_parameter'],
            tau_syn_E=_defaults['tau_syn_E'],
            tau_syn_I=_defaults['tau_syn_I'],
            isyn_exc=_defaults['isyn_exc'],
            isyn_inh=_defaults['isyn_inh'],
            my_neuron_parameter=_defaults['my_neuron_parameter'],
            i_offset=_defaults['i_offset']):
        super(MyModelCurrExpInclInputAndThresholdDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'threshold_value': threshold_value,
            'my_threshold_parameter': my_threshold_parameter,
            'my_multiplicator': my_multiplicator,
            'my_input_parameter': my_input_parameter,
            'tau_syn_E': tau_syn_E, 'tau_syn_I': tau_syn_I,
            'isyn_exc': isyn_exc, 'isyn_inh': isyn_inh,
            'i_offset': i_offset,
            'my_neuron_parameter': my_neuron_parameter,
            'v_init': v_init})

    @staticmethod
    def build_model():
        return MyModelCurrExpInclInputAndThresholdBase
