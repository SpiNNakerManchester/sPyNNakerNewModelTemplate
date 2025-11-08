from spinn_utilities.overrides import overrides
from spinn_utilities.ranged import RangeDictionary
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.implementations import (
    AbstractStandardNeuronComponent)
from spynnaker.pyNN.utilities.struct import Struct

# GLIF3 parameter indices (matching the user's specification)
CM = "c_m"           # Membrane capacitance
EL = "e_l"           # Resting potential
V_RESET = "v_reset"  # Reset voltage
V_THRESH = "v_thresh"  # Threshold voltage
ASC_AMP_0 = "asc_amp_0"  # After-spike current amplitude 0
ASC_AMP_1 = "asc_amp_1"  # After-spike current amplitude 1
G = "g"              # Conductance (1/R)
K0 = "k0"            # After-spike current decay rate 0 (1/tau_0)
K1 = "k1"            # After-spike current decay rate 1 (1/tau_1)
T_REF = "t_ref"      # Refractory period
I_OFFSET = "i_offset"  # Offset current

# State variables
V = "v"              # Membrane voltage
I_ASC_0 = "i_asc_0"  # After-spike current 0
I_ASC_1 = "i_asc_1"  # After-spike current 1


class GLIF3NeuronModel(AbstractStandardNeuronComponent):
    """
    GLIF3 (Generalized Leaky Integrate-and-Fire) neuron model.
    This model includes after-spike currents with exponential decay.

    Model equations:
    dV/dt = (1/C_m) * [I_e + I_asc_0 + I_asc_1 - g*(V - E_L)]
    dI_asc_j/dt = -k_j * I_asc_j, for j = 0, 1

    When V >= V_thresh, spike and reset:
    - V -> V_reset
    - I_asc_j -> I_asc_j * exp(-k_j * t_ref) + asc_amp_j
    """

    def __init__(
            self,
            c_m=1.0,           # Capacitance (nF)
            e_l=-70.0,         # Resting potential (mV)
            v_reset=-70.0,     # Reset voltage (mV)
            v_thresh=-50.0,    # Threshold voltage (mV)
            asc_amp_0=0.0,     # After-spike current amplitude 0 (nA)
            asc_amp_1=0.0,     # After-spike current amplitude 1 (nA)
            g=0.05,            # Conductance (uS)
            k0=0.2,            # ASC decay rate 0 (1/ms)
            k1=0.05,           # ASC decay rate 1 (1/ms)
            t_ref=2.0,         # Refractory period (ms)
            i_offset=0.0,      # Offset current (nA)
            v=-70.0,           # Initial voltage (mV)
            i_asc_0=0.0,       # Initial after-spike current 0 (nA)
            i_asc_1=0.0):      # Initial after-spike current 1 (nA)

        # Define the struct layout - must match C implementation exactly
        super().__init__(
            [Struct([
                (DataType.S1615, V),
                (DataType.S1615, I_ASC_0),
                (DataType.S1615, I_ASC_1),
                (DataType.S1615, CM),
                (DataType.S1615, EL),
                (DataType.S1615, V_RESET),
                (DataType.S1615, V_THRESH),
                (DataType.S1615, ASC_AMP_0),
                (DataType.S1615, ASC_AMP_1),
                (DataType.S1615, G),
                (DataType.S1615, K0),
                (DataType.S1615, K1),
                (DataType.S1615, T_REF),
                (DataType.S1615, I_OFFSET)])],
            {
                CM: "nF", EL: "mV", V_RESET: "mV", V_THRESH: "mV",
                ASC_AMP_0: "nA", ASC_AMP_1: "nA", G: "uS",
                K0: "1/ms", K1: "1/ms", T_REF: "ms", I_OFFSET: "nA",
                V: "mV", I_ASC_0: "nA", I_ASC_1: "nA"
            })

        # Store parameters
        self._c_m = c_m
        self._e_l = e_l
        self._v_reset = v_reset
        self._v_thresh = v_thresh
        self._asc_amp_0 = asc_amp_0
        self._asc_amp_1 = asc_amp_1
        self._g = g
        self._k0 = k0
        self._k1 = k1
        self._t_ref = t_ref
        self._i_offset = i_offset

        # Store state variables
        self._v = v
        self._i_asc_0 = i_asc_0
        self._i_asc_1 = i_asc_1

    # Parameter getters and setters
    @property
    def c_m(self):
        return self._c_m

    @c_m.setter
    def c_m(self, c_m):
        self._c_m = c_m

    @property
    def e_l(self):
        return self._e_l

    @e_l.setter
    def e_l(self, e_l):
        self._e_l = e_l

    @property
    def v_reset(self):
        return self._v_reset

    @v_reset.setter
    def v_reset(self, v_reset):
        self._v_reset = v_reset

    @property
    def v_thresh(self):
        return self._v_thresh

    @v_thresh.setter
    def v_thresh(self, v_thresh):
        self._v_thresh = v_thresh

    @property
    def asc_amp_0(self):
        return self._asc_amp_0

    @asc_amp_0.setter
    def asc_amp_0(self, asc_amp_0):
        self._asc_amp_0 = asc_amp_0

    @property
    def asc_amp_1(self):
        return self._asc_amp_1

    @asc_amp_1.setter
    def asc_amp_1(self, asc_amp_1):
        self._asc_amp_1 = asc_amp_1

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def k0(self):
        return self._k0

    @k0.setter
    def k0(self, k0):
        self._k0 = k0

    @property
    def k1(self):
        return self._k1

    @k1.setter
    def k1(self, k1):
        self._k1 = k1

    @property
    def t_ref(self):
        return self._t_ref

    @t_ref.setter
    def t_ref(self, t_ref):
        self._t_ref = t_ref

    @property
    def i_offset(self):
        return self._i_offset

    @i_offset.setter
    def i_offset(self, i_offset):
        self._i_offset = i_offset

    # State variable getters and setters
    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v

    @property
    def i_asc_0(self):
        return self._i_asc_0

    @i_asc_0.setter
    def i_asc_0(self, i_asc_0):
        self._i_asc_0 = i_asc_0

    @property
    def i_asc_1(self):
        return self._i_asc_1

    @i_asc_1.setter
    def i_asc_1(self, i_asc_1):
        self._i_asc_1 = i_asc_1

    @overrides(AbstractStandardNeuronComponent.add_parameters)
    def add_parameters(self, parameters: RangeDictionary[float]) -> None:
        parameters[CM] = self._c_m
        parameters[EL] = self._e_l
        parameters[V_RESET] = self._v_reset
        parameters[V_THRESH] = self._v_thresh
        parameters[ASC_AMP_0] = self._asc_amp_0
        parameters[ASC_AMP_1] = self._asc_amp_1
        parameters[G] = self._g
        parameters[K0] = self._k0
        parameters[K1] = self._k1
        parameters[T_REF] = self._t_ref
        parameters[I_OFFSET] = self._i_offset

    @overrides(AbstractStandardNeuronComponent.add_state_variables)
    def add_state_variables(
            self, state_variables: RangeDictionary[float]) -> None:
        state_variables[V] = self._v
        state_variables[I_ASC_0] = self._i_asc_0
        state_variables[I_ASC_1] = self._i_asc_1
