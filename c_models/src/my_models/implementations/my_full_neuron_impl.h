#ifndef _MY_FULL_NEURON_IMPL_
#define _MY_FULL_NEURON_IMPL_

// Attempting to demonstrate that a "neuron model" can be defined in a different
// way without the use of components for additional input / input / threshold

#include <neuron/implementations/neuron_impl.h>
#include <spin1_api.h>
#include <debug.h>

//! neuron_impl_t struct
typedef struct neuron_impl_t {
    accum test;
} neuron_impl_t;

//! Array of neuron states
static neuron_impl_t *neuron_array;

static bool neuron_impl_initialise(uint32_t n_neurons) {

    // Allocate DTCM for neuron array
    if (sizeof(neuron_impl_t) != 0) {
        neuron_array = (neuron_impl_t *) spin1_malloc(
            n_neurons * sizeof(neuron_impl_t));
        if (neuron_array == NULL) {
            log_error("Unable to allocate neuron array - Out of DTCM");
            return false;
        }
    }

    return true;
}

static void neuron_impl_add_inputs(
        index_t synapse_type_index, index_t neuron_index,
        input_t weights_this_timestep) {
}

static void neuron_impl_load_neuron_parameters(
        address_t address, uint32_t next, uint32_t n_neurons) {
    spin1_memcpy(neuron_array, &address[next],
        n_neurons * sizeof(neuron_impl_t));

}

static bool neuron_impl_do_timestep_update(
        index_t neuron_index, input_t external_bias,
        state_t *recorded_variable_values) {

    // Get the neuron itself
    neuron_impl_t *neuron = &neuron_array[neuron_index];

    // Return if spiked
    return false;
}

static void neuron_impl_store_neuron_parameters(
        address_t address, uint32_t next, uint32_t n_neurons) {
    spin1_memcpy(&address[next], neuron_array,
        n_neurons * sizeof(neuron_impl_t));
}

#endif // _MY_FULL_NEURON_IMPL_
