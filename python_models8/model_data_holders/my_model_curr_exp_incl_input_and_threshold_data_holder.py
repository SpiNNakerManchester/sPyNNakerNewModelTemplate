# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_exp_incl_input_and_threshold \
    import MyModelCurrExpInclInputAndThresholdBase

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class MyModelCurrExpInclInputAndThresholdDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=(_apv_defs['spikes_per_second']),
            ring_buffer_sigma=(_apv_defs['ring_buffer_sigma']),
            incoming_spike_buffer_size=(
                _apv_defs['incoming_spike_buffer_size']),
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],
            v_init=(
                MyModelCurrExpInclInputAndThresholdBase
                .initialize_parameters['v_init']),
            threshold_value=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'threshold_value']),
            my_threshold_parameter=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'my_threshold_parameter']),
            my_multiplicator=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'my_multiplicator']),
            my_input_parameter=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'my_input_parameter']),
            tau_syn_E=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'tau_syn_E']),
            tau_syn_I=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'tau_syn_I']),
            isyn_exc=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'isyn_exc']),
            isyn_inh=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'isyn_inh']),
            my_neuron_parameter=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'my_neuron_parameter']),
            i_offset=(
                MyModelCurrExpInclInputAndThresholdBase.default_parameters[
                    'i_offset'])):
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
