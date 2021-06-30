#include "my_neuron_model_impl.h"

#include <debug.h>

// The global parameters of this neuron model
const global_neuron_params_t *global_params;

void neuron_model_set_global_neuron_params(
        const global_neuron_params_t *params) {

    // TODO: Store parameters as required
    global_params = params;
}

void neuron_model_print_state_variables(const neuron_t *neuron) {

    // TODO: Print all state variables
    log_debug("V = %11.4k mv", neuron->V);
}

void neuron_model_print_parameters(const neuron_t *neuron) {

    // TODO: Print all neuron parameters
    log_debug("my parameter = %11.4k mv", neuron->my_parameter);
}
