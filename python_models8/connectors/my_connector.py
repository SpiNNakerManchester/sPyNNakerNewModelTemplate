from numpy.typing import NDArray
from typing import Optional,  Sequence
from spinn_utilities.overrides import overrides
from pacman.model.graphs.common import Slice
from spynnaker.pyNN.models.neural_projections import SynapseInformation
from spynnaker.pyNN.types import Weights
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
    def get_delay_maximum(
            self, synapse_info: SynapseInformation) -> float:
        # TODO call self._get_delay_maximum if needed
        return 16

    @overrides(AbstractConnector.get_delay_minimum)
    def get_delay_minimum(
            self, synapse_info: SynapseInformation) -> Optional[float]:
        # TODO call self._get_delay_minimum if needed
        return 1

    @overrides(AbstractGenerateConnectorOnHost.create_synaptic_block)
    def create_synaptic_block(
            self, post_slices: Sequence[Slice], post_vertex_slice: Slice,
            synapse_type: int, synapse_info: SynapseInformation) -> NDArray:
        # TODO: update accordingly
        raise NotImplementedError

    @overrides(AbstractConnector.get_weight_variance)
    def get_weight_variance(self, weights: Weights,
                            synapse_info: SynapseInformation) -> float:
        # TODO: update accordingly
        raise NotImplementedError

    @overrides(AbstractConnector.get_weight_maximum)
    def get_weight_maximum(self, synapse_info: SynapseInformation) -> float:
        # TODO: update accordingly
        raise NotImplementedError

    @overrides(AbstractConnector.get_n_connections_from_pre_vertex_maximum)
    def get_n_connections_from_pre_vertex_maximum(
            self, n_post_atoms: int, synapse_info: SynapseInformation,
            min_delay: Optional[float] = None,
            max_delay: Optional[float] = None) -> int:
        # TODO: update accordingly
        raise NotImplementedError

    @overrides(AbstractConnector.get_n_connections_to_post_vertex_maximum)
    def get_n_connections_to_post_vertex_maximum(
            self, synapse_info: SynapseInformation) -> int:
        # TODO: update accordingly
        raise NotImplementedError
