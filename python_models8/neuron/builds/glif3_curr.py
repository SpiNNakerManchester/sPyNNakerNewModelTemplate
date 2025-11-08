# A PyNN Model for GLIF3 neuron with current-based synapses
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic

# GLIF3-specific components
from python_models8.neuron.neuron_models.glif3_neuron_model import GLIF3NeuronModel
from python_models8.neuron.synapse_types.glif3_synapse_type import GLIF3SynapseType
from spynnaker.pyNN.models.defaults import default_initial_values


class GLIF3Curr(AbstractPyNNNeuronModelStandard):
    """
    GLIF3 (Generalized Leaky Integrate-and-Fire) neuron model with current-based synapses.

    This model includes:
    - Leaky integrate-and-fire dynamics
    - Two after-spike currents with different time constants
    - Fixed threshold
    - 4 independent exponential synapses (AMPA, GABA_A, NMDA, GABA_B)

    Parameters
    ----------
    c_m : float
        Membrane capacitance (nF). Default: 1.0
    e_l : float
        Resting potential (mV). Default: -70.0
    v_reset : float
        Reset voltage after spike (mV). Default: -70.0
    v_thresh : float
        Spike threshold (mV). Default: -50.0
    asc_amp_0 : float
        Fast after-spike current amplitude (nA). Default: 0.0
    asc_amp_1 : float
        Slow after-spike current amplitude (nA). Default: 0.0
    g : float
        Membrane conductance (uS). Default: 0.05
    k0 : float
        Fast after-spike current decay rate (1/ms). Default: 0.2
    k1 : float
        Slow after-spike current decay rate (1/ms). Default: 0.05
    t_ref : float
        Refractory period (ms). Default: 2.0
    i_offset : float
        Offset current (nA). Default: 0.0
    v : float
        Initial membrane voltage (mV). Default: -70.0
    i_asc_0 : float
        Initial fast after-spike current (nA). Default: 0.0
    i_asc_1 : float
        Initial slow after-spike current (nA). Default: 0.0
    tau_syn_0 : float
        Synapse 0 (AMPA - fast excitatory) time constant (ms). Default: 5.0
    tau_syn_1 : float
        Synapse 1 (GABA_A - fast inhibitory) time constant (ms). Default: 5.0
    tau_syn_2 : float
        Synapse 2 (NMDA - slow excitatory) time constant (ms). Default: 5.0
    tau_syn_3 : float
        Synapse 3 (GABA_B - slow inhibitory) time constant (ms). Default: 5.0
    isyn_0 : float
        Initial synaptic current 0 (nA). Default: 0.0
    isyn_1 : float
        Initial synaptic current 1 (nA). Default: 0.0
    isyn_2 : float
        Initial synaptic current 2 (nA). Default: 0.0
    isyn_3 : float
        Initial synaptic current 3 (nA). Default: 0.0
    """

    # Identify which of the values are state variables
    @default_initial_values({"v", "i_asc_0", "i_asc_1", "isyn_0", "isyn_1", "isyn_2", "isyn_3"})
    def __init__(
            self,
            # GLIF3 neuron model parameters
            c_m=1.0,
            e_l=-70.0,
            v_reset=-70.0,
            v_thresh=-50.0,
            asc_amp_0=0.0,
            asc_amp_1=0.0,
            g=0.05,
            k0=0.2,
            k1=0.05,
            t_ref=2.0,
            i_offset=0.0,

            # GLIF3 neuron model state variables
            v=-70.0,
            i_asc_0=0.0,
            i_asc_1=0.0,

            # Synapse type parameters and state variables
            tau_syn_0=5.0,
            tau_syn_1=5.0,
            tau_syn_2=5.0,
            tau_syn_3=5.0,
            isyn_0=0.0,
            isyn_1=0.0,
            isyn_2=0.0,
            isyn_3=0.0):

        # Create GLIF3 neuron model
        neuron_model = GLIF3NeuronModel(
            c_m=c_m,
            e_l=e_l,
            v_reset=v_reset,
            v_thresh=v_thresh,
            asc_amp_0=asc_amp_0,
            asc_amp_1=asc_amp_1,
            g=g,
            k0=k0,
            k1=k1,
            t_ref=t_ref,
            i_offset=i_offset,
            v=v,
            i_asc_0=i_asc_0,
            i_asc_1=i_asc_1)

        # Create synapse type model (4 independent exponential synapses)
        synapse_type = GLIF3SynapseType(
            tau_syn_0=tau_syn_0,
            tau_syn_1=tau_syn_1,
            tau_syn_2=tau_syn_2,
            tau_syn_3=tau_syn_3,
            isyn_0=isyn_0,
            isyn_1=isyn_1,
            isyn_2=isyn_2,
            isyn_3=isyn_3)

        # Create input type model (current-based)
        input_type = InputTypeCurrent()

        # Create threshold type model (static threshold)
        # Note: v_thresh is part of the neuron model, but we need a dummy here
        threshold_type = ThresholdTypeStatic(v_thresh)

        # Create the model using the superclass
        super().__init__(
            # Model name (shown in reports)
            model_name="GLIF3Curr",

            # Matching binary name
            binary="glif3_curr.aplx",

            # Model components
            neuron_model=neuron_model,
            input_type=input_type,
            synapse_type=synapse_type,
            threshold_type=threshold_type)
