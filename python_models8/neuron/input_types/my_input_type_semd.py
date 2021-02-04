from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.input_types import AbstractInputType

MY_MULTIPLICATOR = "my_multiplicator"
MY_INH_INPUT_PREVIOUS = "my_inh_input_previous"

UNITS = {
    MY_MULTIPLICATOR: "0",
    MY_INH_INPUT_PREVIOUS: "mV"
}


class MyInputTypeCurrentSEMD(AbstractInputType):
    """ My current sEMD input type
    """
    __slots__ = [
        "__my_multiplicator",
        "__my_inh_input_previous"]

    def __init__(self, my_multiplicator, my_inh_input_previous):
        super().__init__([
            DataType.S1615,   # my_multiplicator
            DataType.S1615])  # my_inh_input_previous
        self.__my_multiplicator = my_multiplicator
        self.__my_inh_input_previous = my_inh_input_previous

    @overrides(AbstractInputType.get_n_cpu_cycles)
    def get_n_cpu_cycles(self, n_neurons):
        # A bit of a guess
        return 10 * n_neurons

    @overrides(AbstractInputType.add_parameters)
    def add_parameters(self, parameters):
        parameters[MY_MULTIPLICATOR] = self.__my_multiplicator

    @overrides(AbstractInputType.add_state_variables)
    def add_state_variables(self, state_variables):
        state_variables[MY_INH_INPUT_PREVIOUS] = self.__my_inh_input_previous

    @overrides(AbstractInputType.get_units)
    def get_units(self, variable):
        return UNITS[variable]

    @overrides(AbstractInputType.has_variable)
    def has_variable(self, variable):
        return variable in UNITS

    @overrides(AbstractInputType.get_values)
    def get_values(self, parameters, state_variables, vertex_slice, ts):

        # Add the rest of the data
        return [parameters[MY_MULTIPLICATOR],
                state_variables[MY_INH_INPUT_PREVIOUS]]

    @overrides(AbstractInputType.update_values)
    def update_values(self, values, parameters, state_variables):

        # Read the data
        (_my_multiplicator, my_inh_input_previous) = values

        state_variables[MY_INH_INPUT_PREVIOUS] = my_inh_input_previous

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
