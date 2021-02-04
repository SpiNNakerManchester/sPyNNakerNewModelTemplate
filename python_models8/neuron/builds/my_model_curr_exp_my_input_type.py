# A PyNN Model for standard neurons built from components
from spynnaker.pyNN.models.neuron import AbstractPyNNNeuronModelStandard

# Components from main tools
from spynnaker.pyNN.models.neuron.synapse_types.synapse_type_exponential\
    import SynapseTypeExponential
from spynnaker.pyNN.models.neuron.threshold_types.threshold_type_static\
    import ThresholdTypeStatic
from spynnaker.pyNN.models.defaults import default_initial_values

# Additional components
from python_models8.neuron.input_types.my_input_type \
    import MyInputType
from python_models8.neuron.neuron_models.my_neuron_model \
    import MyNeuronModel


class MyModelCurrExpMyInputType(AbstractPyNNNeuronModelStandard):

    @default_initial_values({"v", "isyn_exc", "isyn_inh", "my_multiplicator"})
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

            # input type parameters
            my_multiplicator=0.0,
            my_input_parameter=0.0):

        # create neuron model class
        neuron_model = MyNeuronModel(i_offset, my_neuron_parameter, v)

        # create synapse type model
        synapse_type = SynapseTypeExponential(
            tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)

        # create input type model
        input_type = MyInputType(my_multiplicator, my_input_parameter)

        # create threshold type model
        threshold_type = ThresholdTypeStatic(v_thresh)

        # Create the model using the superclass
        super().__init__(

            # the model a name (shown in reports)
            model_name="MyModelCurrExpMyInputType",

            # the matching binary name
            binary="my_model_curr_exp_my_input_type.aplx",

            # the various model types
            neuron_model=neuron_model, input_type=input_type,
            synapse_type=synapse_type, threshold_type=threshold_type)
