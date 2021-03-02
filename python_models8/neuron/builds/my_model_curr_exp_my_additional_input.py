# A PyNN Model for standard neurons built from components
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeStatic
from spynnaker.pyNN.models.defaults import default_initial_values
from python_models8.neuron.additional_inputs.my_additional_input import (
    MyAdditionalInput)
from python_models8.neuron.neuron_models.my_neuron_model import MyNeuronModel


class MyModelCurrExpMyAdditionalInput(AbstractPyNNNeuronModelStandard):

    @default_initial_values({"v", "isyn_inh", "isyn_exc", "input_current"})
    def __init__(
            self,

            # neuron model parameters and state variables
            my_neuron_parameter=-70.0,
            i_offset=0.0,
            v=-70.0,

            # threshold types parameters
            v_thresh=-50.0,

            # synapse type parameters and state variables
            tau_syn_E=5.0,
            tau_syn_I=5.0,
            isyn_exc=0.0,
            isyn_inh=0.0,

            # additional input parameters and state variables
            my_additional_input_parameter=1.0,
            input_current=0.0):

        # create neuron model class
        neuron_model = MyNeuronModel(i_offset, my_neuron_parameter, v)

        # create synapse type model
        synapse_type = SynapseTypeExponential(
            tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)

        # create input type model
        input_type = InputTypeCurrent()

        # create threshold type model
        threshold_type = ThresholdTypeStatic(v_thresh)

        # create additional inputs
        additional_input_type = MyAdditionalInput(
            my_additional_input_parameter, input_current)

        # Create the model using the superclass
        super().__init__(

            # the model a name (shown in reports)
            model_name="MyModelCurrExpMyAdditionalInput",

            # the matching binary name
            binary="my_model_curr_exp_my_additional_input.aplx",

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type,
            additional_input_type=additional_input_type)
