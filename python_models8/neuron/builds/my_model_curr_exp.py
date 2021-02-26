# A PyNN Model for standard neurons built from components
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic

# Additional components
from python_models8.neuron.neuron_models.my_neuron_model import MyNeuronModel
from spynnaker.pyNN.models.defaults import default_initial_values


class MyModelCurrExp(AbstractPyNNNeuronModelStandard):

    # Identify which of the values are state variables
    @default_initial_values({"v", "isyn_exc", "isyn_inh"})
    def __init__(
            self,

            # neuron model parameters and state variables
            my_neuron_parameter=0.0,
            i_offset=0.0,
            v=-70.0,

            # threshold types parameters
            v_thresh=-50.0,

            # synapse type parameters and state variables
            tau_syn_E=5.0,
            tau_syn_I=5.0,
            isyn_exc=0.0,
            isyn_inh=0.0):

        # create neuron model class
        neuron_model = MyNeuronModel(i_offset, my_neuron_parameter, v)

        # create synapse type model
        synapse_type = SynapseTypeExponential(
            tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = ThresholdTypeStatic(v_thresh)

        # Create the model using the superclass
        super().__init__(

            # the model a name (shown in reports)
            model_name="MyModelCurrExp",

            # the matching binary name
            binary="my_model_curr_exp.aplx",

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
