from typing import Optional, Sequence
from spinn_utilities.overrides import overrides
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.synapse_types import AbstractSynapseType
from spynnaker.pyNN.utilities.struct import Struct
from spynnaker.pyNN.data.spynnaker_data_view import SpynnakerDataView

# TODO: create constants to match the parameter names
EX_SYNAPSE = 'my_ex_synapse_parameter'
IN_SYNAPSE = 'my_in_synapse_parameter'
ISYN_EXC = 'my_exc_init'
ISYN_INH = 'my_inh_init'
TIMESTEP_MS = 'timestep_ms'


class MySynapseType(AbstractSynapseType):
    def __init__(
            self,

            # TODO: update the parameters
            my_ex_synapse_parameter,
            my_in_synapse_parameter,
            my_exc_init,
            my_inh_init):

        # TODO: Update the data types - this must match the struct exactly
        super().__init__(
            [Struct([
                (DataType.S1615, EX_SYNAPSE),
                (DataType.S1615, ISYN_EXC),
                (DataType.S1615, IN_SYNAPSE),
                (DataType.S1615, ISYN_INH),
                (DataType.S1615, TIMESTEP_MS)])],
            {EX_SYNAPSE: "mV", IN_SYNAPSE: 'mV', ISYN_EXC: "", ISYN_INH: ""})

        # TODO: Store the parameters
        self._my_ex_synapse_parameter = my_ex_synapse_parameter
        self._my_in_synapse_parameter = my_in_synapse_parameter
        self._my_exc_init = my_exc_init
        self._my_inh_init = my_inh_init

    # TODO: Add any getters and setters for new parameters

    @property
    def my_ex_synapse_parameter(self):
        return self._my_ex_synapse_parameter

    @my_ex_synapse_parameter.setter
    def my_ex_synapse_parameter(self, my_ex_synapse_parameter):
        self._my_ex_synapse_parameter = my_ex_synapse_parameter

    @property
    def my_in_synapse_parameter(self):
        return self._my_in_synapse_parameter

    @my_in_synapse_parameter.setter
    def my_in_synapse_parameter(self, my_in_synapse_parameter):
        self._my_in_synapse_parameter = my_in_synapse_parameter

    @property
    def my_exc_init(self):
        return self._my_exc_init

    @my_exc_init.setter
    def my_exc_init(self, my_exc_init):
        self._my_exc_init = my_exc_init

    @property
    def my_inh_init(self):
        return self._my_inh_init

    @my_inh_init.setter
    def my_inh_init(self, my_inh_init):
        self._my_inh_init = my_inh_init

    @overrides(AbstractSynapseType.get_n_synapse_types)
    def get_n_synapse_types(self) -> int:
        # TODO: Update with the number of supported synapse types
        return 2

    @overrides(AbstractSynapseType.get_synapse_id_by_target)
    def get_synapse_id_by_target(self, target: str) -> Optional[int]:
        # TODO: update the mapping from name to ID
        if target == "excitatory":
            return 0
        elif target == "inhibitory":
            return 1
        return None

    @overrides(AbstractSynapseType.get_synapse_targets)
    def get_synapse_targets(self) -> Sequence[str]:
        # TODO: update to return the same names as above
        return "excitatory", "inhibitory"

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[EX_SYNAPSE] = self._my_ex_synapse_parameter
        parameters[IN_SYNAPSE] = self._my_in_synapse_parameter
        parameters[TIMESTEP_MS] = (
            SpynnakerDataView.get_simulation_time_step_ms())

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[ISYN_EXC] = self._my_exc_init
        state_variables[ISYN_INH] = self._my_inh_init
