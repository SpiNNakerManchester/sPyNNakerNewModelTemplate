from spinn_utilities.overrides import overrides
from spinn_utilities.ranged import RangeDictionary
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.implementations import (
    AbstractStandardNeuronComponent)
from spynnaker.pyNN.utilities.struct import Struct

# TODO: create constants to match the parameter names
I_OFFSET = "i_offset"
MY_NEURON_PARAMETER = "my_neuron_parameter"
V = "v"


class MyNeuronModel(AbstractStandardNeuronComponent):
    def __init__(
            self,

            # TODO: update the parameters and state variables
            i_offset, my_neuron_parameter, v):

        # TODO: Update the data types - this must match the structs exactly
        super().__init__(
            [Struct([
                (DataType.S1615, V),
                (DataType.S1615, I_OFFSET),
                (DataType.S1615, MY_NEURON_PARAMETER)])],
            {I_OFFSET: "nA", MY_NEURON_PARAMETER: "mV", V: "mV"})

        # TODO: Store any parameters and state variables
        self._i_offset = i_offset
        self._my_neuron_parameter = my_neuron_parameter
        self._v = v

    # TODO: Add getters and setters for the parameters

    @property
    def i_offset(self):
        return self._i_offset

    @i_offset.setter
    def i_offset(self, i_offset):
        self._i_offset = i_offset

    @property
    def my_neuron_parameter(self):
        return self._my_neuron_parameter

    @my_neuron_parameter.setter
    def my_neuron_parameter(self, my_neuron_parameter):
        self._my_neuron_parameter = my_neuron_parameter

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v

    @overrides(AbstractStandardNeuronComponent.add_parameters)
    def add_parameters(self, parameters: RangeDictionary[float]) -> None:
        # TODO: Add initial values of the parameters that the user can change
        parameters[I_OFFSET] = self._i_offset
        parameters[MY_NEURON_PARAMETER] = self._my_neuron_parameter

    @overrides(AbstractStandardNeuronComponent.add_state_variables)
    def add_state_variables(
            self, state_variables: RangeDictionary[float]) -> None:
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[V] = self._v
