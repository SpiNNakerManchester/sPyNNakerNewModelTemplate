# main interface to use the sPyNNaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_my_synapse_type import (
    MyModelCurrMySynapseTypeBase)

_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters
_defaults = MyModelCurrMySynapseTypeBase.default_parameters
_inits = MyModelCurrMySynapseTypeBase.initialize_parameters


class MyModelCurrMySynapseTypeDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs['incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],
            v_init=_inits['v_init'],
            v_thresh=_defaults['v_thresh'],
            my_ex_synapse_parameter=_defaults['my_ex_synapse_parameter'],
            my_in_synapse_parameter=_defaults['my_in_synapse_parameter'],
            my_exc_init=_defaults['my_exc_init'],
            my_inh_init=_defaults['my_inh_init'],
            my_parameter=_defaults['my_parameter'],
            i_offset=_defaults['i_offset']):
        super(MyModelCurrMySynapseTypeDataHolder, self).__init__({
            'spikes_per_second': spikes_per_second,
            'ring_buffer_sigma': ring_buffer_sigma,
            'incoming_spike_buffer_size': incoming_spike_buffer_size,
            'constraints': constraints,
            'label': label,
            'v_thresh': v_thresh,
            'my_ex_synapse_parameter': my_ex_synapse_parameter,
            'my_in_synapse_parameter': my_in_synapse_parameter,
            'my_exc_init': my_exc_init,
            'my_inh_init': my_inh_init,
            'i_offset': i_offset,
            'my_parameter': my_parameter, 'v_init': v_init})

    @staticmethod
    def build_model():
        return MyModelCurrMySynapseTypeBase
