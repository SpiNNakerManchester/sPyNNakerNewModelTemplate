from typing import Optional, Sequence
from spinn_utilities.overrides import overrides
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.synapse_types import AbstractSynapseType
from spynnaker.pyNN.utilities.struct import Struct
from spynnaker.pyNN.data.spynnaker_data_view import SpynnakerDataView

# Parameter and state variable names
TAU_SYN_0 = 'tau_syn_0'
TAU_SYN_1 = 'tau_syn_1'
TAU_SYN_2 = 'tau_syn_2'
TAU_SYN_3 = 'tau_syn_3'
ISYN_0 = 'isyn_0'
ISYN_1 = 'isyn_1'
ISYN_2 = 'isyn_2'
ISYN_3 = 'isyn_3'
TIMESTEP_MS = 'timestep_ms'


class GLIF3SynapseType(AbstractSynapseType):
    """
    Synapse type for GLIF3 model with 4 independent exponential synapses.

    This allows for 4 different receptor types, each with its own time constant.
    All synapses use exponential decay.

    Receptor Types (Allen Institute convention):
    - Type 0 (AMPA): Fast excitatory
    - Type 1 (GABA_A): Fast inhibitory
    - Type 2 (NMDA): Slow excitatory
    - Type 3 (GABA_B): Slow inhibitory

    Parameters
    ----------
    tau_syn_0 : float
        Time constant for synapse type 0 (AMPA) (ms). Default: 5.0
    tau_syn_1 : float
        Time constant for synapse type 1 (GABA_A) (ms). Default: 5.0
    tau_syn_2 : float
        Time constant for synapse type 2 (NMDA) (ms). Default: 5.0
    tau_syn_3 : float
        Time constant for synapse type 3 (GABA_B) (ms). Default: 5.0
    isyn_0 : float
        Initial current for synapse 0 (nA). Default: 0.0
    isyn_1 : float
        Initial current for synapse 1 (nA). Default: 0.0
    isyn_2 : float
        Initial current for synapse 2 (nA). Default: 0.0
    isyn_3 : float
        Initial current for synapse 3 (nA). Default: 0.0
    """

    def __init__(
            self,
            tau_syn_0=5.0,
            tau_syn_1=5.0,
            tau_syn_2=5.0,
            tau_syn_3=5.0,
            isyn_0=0.0,
            isyn_1=0.0,
            isyn_2=0.0,
            isyn_3=0.0):

        # Define the struct layout - must match C implementation exactly
        # Each synapse has: tau (decay), init_input (initial current)
        # Plus timestep_ms for all synapses
        super().__init__(
            [Struct([
                (DataType.S1615, TAU_SYN_0),
                (DataType.S1615, ISYN_0),
                (DataType.S1615, TAU_SYN_1),
                (DataType.S1615, ISYN_1),
                (DataType.S1615, TAU_SYN_2),
                (DataType.S1615, ISYN_2),
                (DataType.S1615, TAU_SYN_3),
                (DataType.S1615, ISYN_3),
                (DataType.S1615, TIMESTEP_MS)])],
            {
                TAU_SYN_0: "ms", TAU_SYN_1: "ms",
                TAU_SYN_2: "ms", TAU_SYN_3: "ms",
                ISYN_0: "nA", ISYN_1: "nA",
                ISYN_2: "nA", ISYN_3: "nA"
            })

        # Store parameters
        self._tau_syn_0 = tau_syn_0
        self._tau_syn_1 = tau_syn_1
        self._tau_syn_2 = tau_syn_2
        self._tau_syn_3 = tau_syn_3

        # Store state variables
        self._isyn_0 = isyn_0
        self._isyn_1 = isyn_1
        self._isyn_2 = isyn_2
        self._isyn_3 = isyn_3

    # Property getters and setters for tau_syn parameters
    @property
    def tau_syn_0(self):
        return self._tau_syn_0

    @tau_syn_0.setter
    def tau_syn_0(self, tau_syn_0):
        self._tau_syn_0 = tau_syn_0

    @property
    def tau_syn_1(self):
        return self._tau_syn_1

    @tau_syn_1.setter
    def tau_syn_1(self, tau_syn_1):
        self._tau_syn_1 = tau_syn_1

    @property
    def tau_syn_2(self):
        return self._tau_syn_2

    @tau_syn_2.setter
    def tau_syn_2(self, tau_syn_2):
        self._tau_syn_2 = tau_syn_2

    @property
    def tau_syn_3(self):
        return self._tau_syn_3

    @tau_syn_3.setter
    def tau_syn_3(self, tau_syn_3):
        self._tau_syn_3 = tau_syn_3

    # Property getters and setters for isyn state variables
    @property
    def isyn_0(self):
        return self._isyn_0

    @isyn_0.setter
    def isyn_0(self, isyn_0):
        self._isyn_0 = isyn_0

    @property
    def isyn_1(self):
        return self._isyn_1

    @isyn_1.setter
    def isyn_1(self, isyn_1):
        self._isyn_1 = isyn_1

    @property
    def isyn_2(self):
        return self._isyn_2

    @isyn_2.setter
    def isyn_2(self, isyn_2):
        self._isyn_2 = isyn_2

    @property
    def isyn_3(self):
        return self._isyn_3

    @isyn_3.setter
    def isyn_3(self, isyn_3):
        self._isyn_3 = isyn_3

    @overrides(AbstractSynapseType.get_n_synapse_types)
    def get_n_synapse_types(self) -> int:
        # 4 synapse types for GLIF3
        return 4

    @overrides(AbstractSynapseType.get_synapse_id_by_target)
    def get_synapse_id_by_target(self, target: str) -> Optional[int]:
        # Map target names to synapse IDs
        # Generic numbered names
        if target == "synapse_0" or target == "syn0":
            return 0
        elif target == "synapse_1" or target == "syn1":
            return 1
        elif target == "synapse_2" or target == "syn2":
            return 2
        elif target == "synapse_3" or target == "syn3":
            return 3
        # Biological receptor names (Allen Institute convention)
        elif target == "AMPA" or target == "ampa":
            return 0  # Fast excitatory
        elif target == "GABA_A" or target == "GABAA" or target == "gaba_a" or target == "gabaa":
            return 1  # Fast inhibitory
        elif target == "NMDA" or target == "nmda":
            return 2  # Slow excitatory
        elif target == "GABA_B" or target == "GABAB" or target == "gaba_b" or target == "gabab":
            return 3  # Slow inhibitory
        # Backward compatibility names
        elif target == "excitatory":
            return 0  # Default to AMPA
        elif target == "inhibitory":
            return 1  # Default to GABA_A
        return None

    @overrides(AbstractSynapseType.get_synapse_targets)
    def get_synapse_targets(self) -> Sequence[str]:
        # Return the 4 synapse target names
        return "synapse_0", "synapse_1", "synapse_2", "synapse_3"

    def add_parameters(self, parameters):
        # Add parameters (time constants)
        parameters[TAU_SYN_0] = self._tau_syn_0
        parameters[TAU_SYN_1] = self._tau_syn_1
        parameters[TAU_SYN_2] = self._tau_syn_2
        parameters[TAU_SYN_3] = self._tau_syn_3
        parameters[TIMESTEP_MS] = (
            SpynnakerDataView.get_simulation_time_step_ms())

    def add_state_variables(self, state_variables):
        # Add state variables (initial synaptic currents)
        state_variables[ISYN_0] = self._isyn_0
        state_variables[ISYN_1] = self._isyn_1
        state_variables[ISYN_2] = self._isyn_2
        state_variables[ISYN_3] = self._isyn_3
