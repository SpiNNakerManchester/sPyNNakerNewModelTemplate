from spynnaker.pyNN.models.neuron.input_types import AbstractInputType
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.utilities.struct import Struct

# TODO create constants to match the parameter names
MY_MULTIPLICATOR = "my_multiplicator"
MY_INPUT_PARAMETER = "my_input_parameter"


class MyInputType(AbstractInputType):

    def __init__(
            self,

            # TODO: update the parameters
            my_multiplicator,
            my_input_parameter):

        # TODO: Update the data types
        super().__init__([
            Struct([
                (DataType.S1615, MY_MULTIPLICATOR),
                (DataType.S1615, MY_INPUT_PARAMETER)])],
            {MY_MULTIPLICATOR: "", MY_INPUT_PARAMETER: "mA"})

        # TODO: store the parameters
        self._my_multiplicator = my_multiplicator
        self._my_input_parameter = my_input_parameter

    # TODO: Add getters and setters for the parameters

    @property
    def my_multiplicator(self):
        return self._my_multiplicator

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self._my_multiplicator = my_multiplicator

    @property
    def my_input_parameter(self):
        return self._my_input_parameter

    @my_input_parameter.setter
    def my_input_parameter(self, my_input_parameter):
        self._my_input_parameter = my_input_parameter

    def get_global_weight_scale(self):
        return 1.0

    def add_parameters(self, parameters):
        # TODO: Add initial values of the parameters that the user can change
        parameters[MY_INPUT_PARAMETER] = self._my_input_parameter

    def add_state_variables(self, state_variables):
        # TODO: Add initial values of the state variables that the user can
        # change
        state_variables[MY_MULTIPLICATOR] = self._my_multiplicator
