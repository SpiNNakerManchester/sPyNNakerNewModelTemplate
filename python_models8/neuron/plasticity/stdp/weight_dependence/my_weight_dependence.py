from spinn_utilities.overrides import overrides
from data_specification.enums import DataType
from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence\
    import AbstractWeightDependence
from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence\
    import AbstractHasAPlusAMinus


class MyWeightDependence(AbstractWeightDependence, AbstractHasAPlusAMinus):

    def __init__(
            self,

            # TODO: update the parameters
            w_min=0.0, w_max=1.0, my_parameter=0.1):

        AbstractWeightDependence.__init__(self)
        AbstractHasAPlusAMinus.__init__(self)

        # TODO: Store any parameters
        self._w_min = w_min
        self._w_max = w_max
        self._my_parameter = my_parameter

    # TODO: Add getters and setters for the parameters

    @property
    def w_min(self):
        return self._w_min

    @w_min.setter
    def w_min(self, w_min):
        self._w_min = w_min

    @property
    def w_max(self, w_max):
        return self._w_max

    @w_max.setter
    def w_max(self, w_max):
        self._w_max = w_max

    @property
    def my_parameter(self):
        return self._my_parameter

    @my_parameter.setter
    def my_parameter(self, my_parameter):
        self._my_parameter = my_parameter

    def is_same_as(self, weight_dependence):

        # TODO: Update with the correct class name
        if not isinstance(weight_dependence, MyWeightDependence):
            return False

        # TODO: update to check parameters are equal
        return (
            (self._w_min == weight_dependence._w_min) and
            (self._w_max == weight_dependence._w_max) and
            (self._my_parameter == weight_dependence._my_parameter))

    @property
    def vertex_executable_suffix(self):
        # TODO: Add the extension to be added to the binary executable name
        # to indicate that it is compiled with this weight dependence
        # Note: The expected format of the binary name is:
        #    <neuron_model>_stdp[_mad|]_<timing_dependence>_<weight_dependence>
        return "my_weight"

    def get_parameters_sdram_usage_in_bytes(
            self, n_synapse_types, n_weight_terms):

        # TODO: update to match the number of bytes used by the parameters
        if n_weight_terms == 1:
            return 12 * n_synapse_types
        else:
            raise NotImplementedError(
                "My weight dependence only supports one term")

    def write_parameters(
            self, spec, machine_time_step, weight_scales, n_weight_terms):

        # TODO: update to write the parameters
        # Loop through each synapse type's weight scale
        for w in weight_scales:

            # Scale the maximum and minimum weights to fixed-point values
            # based on the weight scaling that has been done externally
            spec.write_value(
                data=int(round(self._w_min * w)), data_type=DataType.INT32)
            spec.write_value(
                data=int(round(self._w_max * w)), data_type=DataType.INT32)

            # Write my parameter as an appropriately scaled fixed-point number
            spec.write_value(
                data=int(round(self._my_parameter * w)),
                data_type=DataType.INT32)

            if n_weight_terms != 1:
                raise NotImplementedError(
                    "My weight dependence only supports one term")

    @property
    def weight_maximum(self):

        # TODO: update to return the maximum weight that this rule will ever
        # give to a synapse
        return self._w_max

    @overrides(AbstractWeightDependence.get_parameter_names)
    def get_parameter_names(self):
        return ['w_min', 'w_max', 'my_parameter']
