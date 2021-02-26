from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModel
from spynnaker.pyNN.models.defaults import default_parameters
from python_models8.neuron.implementations.my_full_neuron_impl import (
    MyFullNeuronImpl)


class MyFullNeuron(AbstractPyNNNeuronModel):

    @default_parameters({"threshold"})
    def __init__(self, threshold=10.0, v=0.0, exc_input=0.0, inh_input=0.0):
        super().__init__(MyFullNeuronImpl(threshold, v, exc_input, inh_input))
