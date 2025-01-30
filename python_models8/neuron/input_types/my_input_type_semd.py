from spinn_utilities.overrides import overrides
from spinn_utilities.ranged import RangeDictionary
from spinn_front_end_common.interface.ds import DataType
from spynnaker.pyNN.models.neuron.input_types import AbstractInputType
from spynnaker.pyNN.utilities.struct import Struct

MY_MULTIPLICATOR = "my_multiplicator"
MY_INH_INPUT_PREVIOUS = "my_inh_input_previous"


class MyInputTypeCurrentSEMD(AbstractInputType):
    """ My current sEMD input type
    """
    __slots__ = [
        "__my_multiplicator",
        "__my_inh_input_previous"]

    def __init__(self, my_multiplicator, my_inh_input_previous):
        super().__init__([
            Struct([
                (DataType.S1615, MY_MULTIPLICATOR),
                (DataType.S1615, MY_INH_INPUT_PREVIOUS)])],
            {MY_MULTIPLICATOR: "0", MY_INH_INPUT_PREVIOUS: "mV"})
        self.__my_multiplicator = my_multiplicator
        self.__my_inh_input_previous = my_inh_input_previous

    @overrides(AbstractInputType.add_parameters)
    def add_parameters(self, parameters: RangeDictionary[float]) -> None:
        parameters[MY_MULTIPLICATOR] = self.__my_multiplicator

    @overrides(AbstractInputType.add_state_variables)
    def add_state_variables(
            self, state_variables: RangeDictionary[float]) -> None:
        state_variables[MY_INH_INPUT_PREVIOUS] = self.__my_inh_input_previous

    @property
    def my_multiplicator(self):
        return self.__my_multiplicator

    @my_multiplicator.setter
    def my_multiplicator(self, my_multiplicator):
        self.__my_multiplicator = my_multiplicator

    @property
    def my_inh_input_previous(self):
        return self.__my_inh_input_previous

    @my_inh_input_previous.setter
    def my_inh_input_previous(self, my_inh_input_previous):
        self.__my_inh_input_previous = my_inh_input_previous

    def get_global_weight_scale(self):
        return 1.0
