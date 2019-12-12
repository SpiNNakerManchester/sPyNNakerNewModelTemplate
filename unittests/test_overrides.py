import unittest
from python_models8.neuron.additional_inputs.my_additional_input import (
    MyAdditionalInput)
from python_models8.neuron.implementations.my_full_neuron_impl import (
    MyFullNeuronImpl)
from python_models8.neuron.input_types.my_input_type import MyInputType
from python_models8.neuron.input_types.my_input_type_semd import (
    MyInputTypeCurrentSEMD)
from python_models8.neuron.neuron_models.my_neuron_model import MyNeuronModel
from python_models8.neuron.plasticity.stdp.timing_dependence.\
    my_timing_dependence import MyTimingDependence
from python_models8.neuron.plasticity.stdp.weight_dependence.\
    my_weight_dependence import MyWeightDependence
from python_models8.neuron.synapse_types.my_synapse_type import MySynapseType
from python_models8.neuron.threshold_types.my_threshold_type import (
    MyThresholdType)


class TestOverrides(unittest.TestCase):
    """
    Tests to trigger the overides check.

    The None parameters is due to lazyiness and not as an example usage.
    """

    def test_my_additional_input(self):
        MyAdditionalInput(None, None)

    def test_my_full_neuron_impl(self):
        MyFullNeuronImpl(None, None, None, None)

    def test_my_input_type(self):
        MyInputType(None, None)

    def test_input_types(self):
        MyInputTypeCurrentSEMD(None, None)

    def test_my_neuron_model(self):
        MyNeuronModel(None, None, None)

    def test_my_timing_dependence(self):
        MyTimingDependence(None, None)

    def test_my_weight_dependence(self):
        MyWeightDependence()

    def test_my_synapse_type(self):
        MySynapseType(None, None, None, None)

    def my_threshold_type(self):
        MyThresholdType()