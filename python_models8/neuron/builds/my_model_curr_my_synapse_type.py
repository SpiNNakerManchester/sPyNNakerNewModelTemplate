# A PyNN Model for standard neurons built from components
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic
from spynnaker.pyNN.models.defaults import default_initial_values

# Additional components
from python_models8.neuron.neuron_models.my_neuron_model import MyNeuronModel
from python_models8.neuron.synapse_types.my_synapse_type import MySynapseType


class MyModelCurrMySynapseType(AbstractPyNNNeuronModelStandard):

    @default_initial_values({"v", "my_exc_init", "my_inh_init"})
    def __init__(
            self,

            # neuron model parameters and state variables
            my_neuron_parameter=-70.0,
            i_offset=0.0,
            v=-70.0,

            # threshold types parameters
            v_thresh=-50.0,

            # synapse type parameters and state variables
            my_ex_synapse_parameter=0.1,
            my_in_synapse_parameter=0.1,
            my_exc_init=0.0,
            my_inh_init=0.0):

        # create neuron model class
        neuron_model = MyNeuronModel(i_offset, my_neuron_parameter, v)

        # create synapse type model
        synapse_type = MySynapseType(
            my_ex_synapse_parameter, my_in_synapse_parameter,
            my_exc_init, my_inh_init)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = ThresholdTypeStatic(v_thresh)

        # instantiate the sPyNNaker system by initialising
        # the AbstractPopulationVertex
        super().__init__(

            # the model a name (shown in reports)
            model_name="MyModelMySynapseType",

            # the matching binary name
            binary="my_model_curr_my_synapse_type.aplx",

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
