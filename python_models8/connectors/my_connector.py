from spinn_utilities.overrides import overrides
from spynnaker.pyNN.models.neural_projections.connectors import (
    AbstractConnector, AbstractGenerateConnectorOnHost)


class MyConnector(AbstractConnector, AbstractGenerateConnectorOnHost):
    """ Connects two vertices with some thing.
    """

    def __init__(self, weights=0.0, delays=1, allow_self_connections=True
                 # TODO: Add your parameters here
                 ):
        """ Creates a new MyConnector

        :param weights: The weight of the connector.
        :type weights: float or iterable(float)
        :param delays: The inherent delay of the connector, in ms.
        :type delays: float or iterable(float)
        :param bool allow_self_connections:
            Whether this connector allows a vertex to connect to itself.
        """
        super().__init__()
        self._weights = weights
        self._delays = delays
        self._allow_self_connections = allow_self_connections

        # TODO: Store any additional parameters

    @overrides(AbstractConnector.get_delay_maximum)
    def get_delay_maximum(self, synapse_info):
        # TODO call self._get_delay_maximum if needed
        return 16

    @overrides(AbstractConnector.get_delay_minimum)
    def get_delay_minimum(self, synapse_info):
        # TODO call self._get_delay_minimum if needed
        return 1

    @overrides(AbstractGenerateConnectorOnHost.create_synaptic_block)
    def create_synaptic_block(
            self, post_slices, post_vertex_slice, synapse_type, synapse_info):
        # TODO: update accordingly
        pass

    @overrides(AbstractConnector.get_weight_variance)
    def get_weight_variance(
            self, weights, synapse_info):
        # TODO: update accordingly
        pass

    @overrides(AbstractConnector.get_weight_maximum)
    def get_weight_maximum(self, synapse_info):
        # TODO: update accordingly
        pass

    @overrides(AbstractConnector.get_n_connections_from_pre_vertex_maximum)
    def get_n_connections_from_pre_vertex_maximum(
            self, n_post_atoms, synapse_info, min_delay=None,
            max_delay=None):
        # TODO: update accordingly
        pass

    @overrides(AbstractConnector.get_n_connections_to_post_vertex_maximum)
    def get_n_connections_to_post_vertex_maximum(self, synapse_info):
        # TODO: update accordingly
        pass
