from spynnaker.pyNN.models.defaults import default_initial_values
from spynnaker.pyNN.models.neuron.neuron_models import (
    NeuronModelLeakyIntegrateAndFire)
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard
from spynnaker.pyNN.models.neuron.implementations import ModelParameter
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential
from python_models8.neuron.input_types.my_input_type_semd import (
    MyInputTypeCurrentSEMD)
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic


class MyIFCurrExpSEMD(AbstractPyNNNeuronModelStandard):
    """ Leaky integrate and fire neuron with an exponentially decaying \
        current input, where the excitatory input depends upon the inhibitory
        input (see https://www.cit-ec.de/en/nbs/spiking-insect-vision)
        Note: this is an older version of the sEMD model in sPyNNaker that
        required a new implementation C file in order to make it work.
    """

    @default_initial_values({"v", "isyn_exc", "isyn_inh",
                             "my_inh_input_previous"})
    def __init__(
            self, tau_m: ModelParameter = 20.0, cm: ModelParameter = 1.0,
            v_rest: ModelParameter = -65.0, v_reset: ModelParameter = -65.0,
            v_thresh: ModelParameter = -50.0, tau_syn_E: ModelParameter = 5.0,
            tau_syn_I: ModelParameter = 5.0, tau_refrac: ModelParameter = 0.1,
            i_offset: ModelParameter = 0.0, v: ModelParameter = -65.0,
            isyn_exc: ModelParameter = 0.0, isyn_inh: ModelParameter = 0.0,
            my_multiplicator: ModelParameter = 0.0,
            my_inh_input_previous: ModelParameter = 0.0):

        neuron_model = NeuronModelLeakyIntegrateAndFire(
            v, v_rest, tau_m, cm, i_offset, v_reset, tau_refrac)
        synapse_type = SynapseTypeExponential(
            tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)
        input_type = MyInputTypeCurrentSEMD(
            my_multiplicator, my_inh_input_previous)
        threshold_type = ThresholdTypeStatic(v_thresh)

        super().__init__(
            model_name="my_if_curr_exp_sEMD",
            binary="my_if_curr_exp_sEMD.aplx",
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
