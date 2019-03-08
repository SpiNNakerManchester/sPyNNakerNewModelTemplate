from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModel
from spynnaker.pyNN.models.defaults import default_parameters
from python_models8.neuron.implementations.drl_lif_neuron_impl \
    import DRLLIFNeuronImpl


class DRLLIFNeuron(AbstractPyNNNeuronModel):

    @default_parameters({"threshold"})
    def __init__(self, threshold=-55.0, v=-65.0, exc_input=0.0, inh_input=0.0):
        AbstractPyNNNeuronModel.__init__(
            self, DRLLIFNeuronImpl(threshold, v, exc_input, inh_input))
