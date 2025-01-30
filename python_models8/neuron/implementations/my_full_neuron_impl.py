from typing import List, Mapping, Optional
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.utilities.struct import Struct
from spynnaker.pyNN.models.neuron.implementations import (
    AbstractNeuronImpl)
from spinn_utilities.overrides import overrides
from spinn_utilities.ranged import RangeDictionary

# TODO: Add names for parameters and state variables
THRESHOLD = "threshold"
V = "v"
EXC_INPUT = "exc_input"
INH_INPUT = "inh_input"

# TODO: Update the units for the parameters and state variables
UNITS = {
    THRESHOLD: "mV",
    V: "mV",
    EXC_INPUT: "nA",
    INH_INPUT: "nA"
}


class MyFullNeuronImpl(AbstractNeuronImpl):

    def __init__(self,

                 # TODO: add model parameters and state variables
                 threshold, v, exc_input, inh_input):

        # TODO: Store the variables
        self._threshold = threshold
        self._v = v
        self._exc_input = exc_input
        self._inh_input = inh_input

        # TODO: Store a struct to make other operations easier
        self._struct = Struct([
            (DataType.S1615, EXC_INPUT),
            (DataType.S1615, INH_INPUT),
            (DataType.S1615, V),
            (DataType.S1615, THRESHOLD)])

    @property
    @overrides(AbstractNeuronImpl.structs)
    def structs(self) -> List[Struct]:
        return [self._struct]

    @property
    @overrides(AbstractNeuronImpl.model_name)
    def model_name(self) -> str:
        # TODO: Update the name
        return "MyFullNeuronImpl"

    @property
    @overrides(AbstractNeuronImpl.binary_name)
    def binary_name(self) -> str:
        # TODO: Update the binary name
        return "my_full_neuron_impl.aplx"

    @overrides(AbstractNeuronImpl.get_global_weight_scale)
    def get_global_weight_scale(self) -> float:
        # TODO: Update if a weight scale is required
        return 1.0

    @overrides(AbstractNeuronImpl.get_n_synapse_types)
    def get_n_synapse_types(self) -> int:
        # TODO: Update to the number of synapse types your model uses
        # (this is the inputs array in this model)
        return 2

    @overrides(AbstractNeuronImpl.get_synapse_id_by_target)
    def get_synapse_id_by_target(self, target: str) -> Optional[int]:
        # TODO: Update with the names that are allowed on a PyNN synapse
        # receptor_type and match up with indices
        if target == "excitatory":
            return 0
        elif target == "inhibitory":
            return 1
        raise ValueError("Unknown target {}".format(target))

    @overrides(AbstractNeuronImpl.get_synapse_targets)
    def get_synapse_targets(self) -> List[str]:

        # TODO: Update with the names that are allowed on a PyNN synapse
        # receptor_type
        return ["excitatory", "inhibitory"]

    @overrides(AbstractNeuronImpl.get_recordable_variables)
    def get_recordable_variables(self) -> List[str]:
        # TODO: Update with the names of state variables that can be recorded
        return ["v"]

    @overrides(AbstractNeuronImpl.get_recordable_data_types)
    def get_recordable_data_types(self) -> Mapping[str, DataType]:
        # TODO: Update with the names and recorded types of the state variables
        return {"v": DataType.S1615}

    @overrides(AbstractNeuronImpl.get_recordable_units)
    def get_recordable_units(self, variable: str) -> str:
        # TODO: Update with the appropriate units for variables
        if variable != "v":
            raise ValueError("Unknown variable {}".format(variable))
        return "mV"

    @overrides(AbstractNeuronImpl.get_recordable_variable_index)
    def get_recordable_variable_index(self, variable: str) -> int:
        # TODO: Update with the index in the recorded_variable_values array
        # that the given variable will be recorded in to
        if variable != "v":
            raise ValueError("Unknown variable {}".format(variable))
        return 0

    @overrides(AbstractNeuronImpl.is_recordable)
    def is_recordable(self, variable: str) -> bool:
        # TODO: Update to identify variables that can be recorded
        return variable == "v"

    @overrides(AbstractNeuronImpl.add_parameters)
    def add_parameters(self, parameters: RangeDictionary) -> None:
        # TODO: Write the parameter values
        parameters[THRESHOLD] = self._threshold

    @overrides(AbstractNeuronImpl.add_state_variables)
    def add_state_variables(self, state_variables: RangeDictionary) -> None:
        # TODO: Write the state variable values
        state_variables[V] = self._v
        state_variables[EXC_INPUT] = self._exc_input
        state_variables[INH_INPUT] = self._inh_input

    @overrides(AbstractNeuronImpl.get_units)
    def get_units(self, variable: str) -> str:
        # This uses the UNITS dict so shouldn't need to be updated
        return UNITS[variable]

    @property
    @overrides(AbstractNeuronImpl.is_conductance_based)
    def is_conductance_based(self) -> bool:
        # TODO: Update if uses conductance
        return False
