from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModel
from spynnaker.pyNN.models.defaults import default_parameters
from python_models8.neuron.implementations.recording_neuron_impl \
    import RecordingNeuronImpl


class RecordingNeuron(AbstractPyNNNeuronModel):

    @default_parameters({"threshold"})
    def __init__(self, threshold=10.0, v=0.0, exc_input=0.0, inh_input=0.0):
        AbstractPyNNNeuronModel.__init__(
            self, RecordingNeuronImpl(threshold, v, exc_input, inh_input))
