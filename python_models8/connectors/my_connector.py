from spynnaker.pyNN.models.neural_projections.connectors \
    import AbstractConnector


class MyConnector(AbstractConnector):
    """
    Connects two vertices with some thing

    """

    def __init__(self, weights=0.0, delays=1, allow_self_connections=True
                 # TODO: Add your parameters here
                 ):
        """
        Creates a new MyConnector
        """
        AbstractConnector.__init__(self)
        self._weights = weights
        self._delays = delays
        self._allow_self_connections = allow_self_connections

        # TODO: Store any additional parameters

    def get_delay_maximum(self):
        """ Get the maximum delay specified by the user in ms, or None if\
            unbounded
        """
        # TODO: update accordingly
        return 16

    def create_synaptic_block(self, pre_slices, pre_slice_index, post_slices,
                              post_slice_index, pre_vertex_slice,
                              post_vertex_slice, synapse_type):
        """ Create a synaptic block from the data
        """

        # TODO: update accordingly
        pass

    def get_weight_variance(self, pre_slices, pre_slice_index, post_slices,
                            post_slice_index, pre_vertex_slice,
                            post_vertex_slice):
        """ Get the variance of the weights
        """
        # TODO: update accordingly
        pass

    def generate_on_machine(self):
        """ Determines if the connector generation is supported on the machine\
            or if the connector must be generated on the host
        """
        # TODO: update accordingly
        pass

    def get_weight_maximum(self, pre_slices, pre_slice_index, post_slices,
                           post_slice_index, pre_vertex_slice,
                           post_vertex_slice):
        """ Get the maximum of the weights for this connection
        """
        # TODO: update accordingly
        pass

    def get_n_connections_to_post_vertex_maximum(self, pre_slices,
                                                 pre_slice_index, post_slices,
                                                 post_slice_index,
                                                 pre_vertex_slice,
                                                 post_vertex_slice):
        """ Get the maximum number of connections between those from each of\
            the neurons in the pre_vertex_slice to neurons in the\
            post_vertex_slice, for connections with a delay between min_delay\
            and max_delay (inclusive) if both specified\
            (otherwise all connections)
        """
        # TODO: update accordingly
        pass

    def get_weight_mean(self, pre_slices, pre_slice_index, post_slices,
                        post_slice_index, pre_vertex_slice, post_vertex_slice):
        """ Get the mean of the weights for this connection
        """
        # TODO: update accordingly
        pass

    def get_n_connections_from_pre_vertex_maximum(self, pre_slices,
                                                  pre_slice_index, post_slices,
                                                  post_slice_index,
                                                  pre_vertex_slice,
                                                  post_vertex_slice,
                                                  min_delay=None,
                                                  max_delay=None):
        """ Get the maximum number of connections between those to each of the\
            neurons in the post_vertex_slice from neurons in the\
            pre_vertex_slice
        """
        # TODO: update accordingly
        pass
