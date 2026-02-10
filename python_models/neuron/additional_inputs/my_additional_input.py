from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.additional_inputs import (
    AbstractAdditionalInput)
from spynnaker.pyNN.utilities.struct import Struct

# TODO: create constants to match the parameter names
MY_ADDITIONAL_INPUT_PARAMETER = "my_additional_input_parameter"
INPUT_CURRENT = "input_current"

# TODO: create units for each parameter
UNITS = {
    MY_ADDITIONAL_INPUT_PARAMETER: "nA",
    INPUT_CURRENT: "nA"
}


class MyAdditionalInput(AbstractAdditionalInput):

    def __init__(
            self,

            # TODO: update the parameters
            my_additional_input_parameter, input_current):

        # TODO: Update the data types - this must match the struct exactly
        super().__init__(
            [Struct([
                (DataType.S1615, MY_ADDITIONAL_INPUT_PARAMETER),
                (DataType.S1615, INPUT_CURRENT)])],
            {MY_ADDITIONAL_INPUT_PARAMETER: "nA", INPUT_CURRENT: "nA"})

        # TODO: store the parameters
        self._my_additional_input_parameter = my_additional_input_parameter
        self._input_current = input_current

    # TODO: Add getters and setters for the parameters

    @property
    def my_additional_input_parameter(self):
        return self._my_additional_input_parameter

    @my_additional_input_parameter.setter
    def my_additional_input_parameter(self, my_additional_input_parameter):
        self._my_additional_input_parameter = my_additional_input_parameter

    @property
    def input_current(self):
        return self._input_current

    @input_current.setter
    def input_current(self, input_current):
        self._input_current = input_current

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters
        parameters[MY_ADDITIONAL_INPUT_PARAMETER] = (
            self._my_additional_input_parameter)

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables
        state_variables[INPUT_CURRENT] = self._input_current
