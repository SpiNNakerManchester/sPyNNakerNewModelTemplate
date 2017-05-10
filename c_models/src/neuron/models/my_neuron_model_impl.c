#include "my_neuron_model_impl.h"

#include <debug.h>

static global_neuron_params_pointer_t global_params;

void neuron_model_set_global_neuron_params(
        global_neuron_params_pointer_t params) {

    // TODO: Store parameters as required
    global_params = params;
}

state_t neuron_model_state_update(
        input_t exc_input, input_t inh_input, input_t external_bias,
        neuron_pointer_t neuron) {

    // This takes the input and generates an input value, assumed to be a
    // current.  Note that the conversion to current from conductance is done
    // outside of this function, so does not need to be repeated here.
    input_t input_this_timestep =
        exc_input - inh_input + external_bias + neuron->I_offset;


    // TODO: Solve your equation here
    neuron->V += input_this_timestep;

    log_info("TESTING TESTING V = %11.4k mv", neuron->V);

    // Return the state variable to be compared with the threshold value
    // to determine if the neuron has spikes (commonly the membrane voltage)
    // TODO: Update to return the correct variable
    return neuron->V;
}

state_t neuron_model_get_membrane_voltage(neuron_pointer_t neuron) {

    // TODO: Get the state value representing the membrane voltage
    return neuron->V;
}

void neuron_model_has_spiked(neuron_pointer_t neuron) {

    // TODO: Perform operations required to reset the state after a spike
    neuron->V = neuron->my_parameter;
}

void neuron_model_print_state_variables(restrict neuron_pointer_t neuron) {

    // TODO: Print all state variables
    log_debug("V = %11.4k mv", neuron->V);
}

void neuron_model_print_parameters(restrict neuron_pointer_t neuron) {

    // TODO: Print all neuron parameters
    log_debug("my parameter = %11.4k mv", neuron->my_parameter);
}
