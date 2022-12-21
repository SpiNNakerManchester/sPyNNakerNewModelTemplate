/*! \file
 * \brief implementation of synapse_types.h for Exponential shaping
*
* \details This is used to give a simple exponential decay to synapses.
*
* If we have combined excitatory/inhibitory synapses it will be
* because both excitatory and inhibitory synaptic time-constants
* (and thus propogators) are identical.
*/


#ifndef _SYNAPSE_TYPES_MY_IMPL_H_
#define _SYNAPSE_TYPES_MY_IMPL_H_

// This is used for exponential synapses
#include <neuron/synapse_types/exp_synapse_utils.h>
#include <debug.h>

// TODO: Determine the number of bits required by the synapse type in the
// synapse row data structure (i.e. enough bits to represent all desired
// synapse types)
// e.g. 1 bit for 2 possible types such as excitatory and inhibitory
// This must match the number returned by the python method
// get_n_synapse_type_bits
#define SYNAPSE_TYPE_BITS 1

// TODO: Determine the number of synapse types required
// (e.g. 2 for excitatory and inhibitory)]
// This must match the number returned by the python method
// get_n_synapse_types
#define SYNAPSE_TYPE_COUNT 2

// TODO: Define the parameters required to compute the synapse shape
// Note this must match up with the Python code.
struct synapse_types_params_t {
    exp_params_t my_exc;
    exp_params_t my_inh;
    REAL time_step_ms;
};

// TODO: Define the state required to compute the synapse shape
// Note that this may or differ from the parameters if things are computed.
struct synapse_types_t {
    exp_state_t my_exc;
    exp_state_t my_inh;
};

// Define receptor split
#define NUM_EXCITATORY_RECEPTORS 1
#define NUM_INHIBITORY_RECEPTORS 1

// Include this here after defining the above items
#include <neuron/synapse_types/synapse_types.h>

// This makes it easy to keep track of which is which
typedef enum input_buffer_regions {
    EXCITATORY, INHIBITORY,
} input_buffer_regions;

static inline void synapse_types_initialise(synapse_types_t *state,
        synapse_types_params_t *params, uint32_t n_steps_per_timestep) {
    decay_and_init(&state->my_exc, &params->my_exc, params->time_step_ms, n_steps_per_timestep);
    decay_and_init(&state->my_inh, &params->my_inh, params->time_step_ms, n_steps_per_timestep);
}

static inline void synapse_types_save_state(synapse_types_t *state,
        synapse_types_params_t *params) {
    params->my_exc.init_input = state->my_exc.synaptic_input_value;
    params->my_inh.init_input = state->my_inh.synaptic_input_value;
}

//! \brief Shapes the values input into the neurons
//! \param[in] pointer to parameters the synapse parameter pointer passed in
//! \return Nothing
static inline void synapse_types_shape_input(
        synapse_types_t *parameters) {
    exp_shaping(&parameters->my_exc);
    exp_shaping(&parameters->my_inh);
}


//! \brief Adds the initial value to an input buffer for this shaping.  Allows
//         the input to be scaled before being added.
//! \param[in-out] input_buffers the pointer to the input buffers
//! \param[in] synapse_type_index the index of the synapse type to add the
//                                value to
//! \param[in] pointer to parameters the synapse parameters passed in
//! \param[in] input the input to be added
//! \return None
static inline void synapse_types_add_neuron_input(
        index_t synapse_type_index, synapse_types_t *parameters,
        input_t input) {
    if (synapse_type_index == EXCITATORY) {
        add_input_exp(&parameters->my_exc, input);
    } else if (synapse_type_index == INHIBITORY) {
        add_input_exp(&parameters->my_inh, input);
    }
}

//! \brief Gets the excitatory input for a given neuron
//! \param[in] pointer to parameters the synapse parameters passed in
//! \return the first entry in the array of excitatory input values
static inline input_t* synapse_types_get_excitatory_input(
        input_t *excitatory_response, synapse_types_t *parameters) {
    excitatory_response[0] = parameters->my_exc.synaptic_input_value;
    return &excitatory_response[0];
}

//! \brief Gets the inhibitory input for a given neuron
//! \param[in] pointer to parameters the synapse parameters passed in
//! \return the first entry in array of inhibitory input values
static inline input_t* synapse_types_get_inhibitory_input(
        input_t *inhibitory_response, synapse_types_t *parameters) {
    inhibitory_response[0] = parameters->my_inh.synaptic_input_value;
    return &inhibitory_response[0];
}

//! \brief returns a human readable character for the type of synapse, for
//         debug purposes
//! examples would be X = excitatory types, I = inhibitory types etc etc.
//! \param[in] synapse_type_index the synapse type index
//! \return a human readable character representing the synapse type.
static inline const char *synapse_types_get_type_char(
        index_t synapse_type_index) {

    // TODO: Update with your synapse types
    if (synapse_type_index == EXCITATORY) {
        return "X";
    } else if (synapse_type_index == INHIBITORY)  {
        return "I";
    } else {
        log_debug("Did not recognise synapse type %i", synapse_type_index);
        return "?";
    }
}

//! \brief prints the input for a neuron ID for debug purposes
//! \param[in] pointer to parameters the synapse parameters passed in
//! \return Nothing
static inline void synapse_types_print_input(
        synapse_types_t *parameters) {
    io_printf(IO_BUF, "%12.6k - %12.6k",
            parameters->my_exc.synaptic_input_value,
            parameters->my_inh.synaptic_input_value);
    // TODO: Does this function need the remaining parameters adding to it?
}

//! \brief print parameters call
//! \param[in] parameter: the pointer to the parameters to print
//! \return Nothing
static inline void synapse_types_print_parameters(
        synapse_types_t *parameters) {

    // TODO: Update to print your parameters
    log_info("my_exc_decay = %R\n", (unsigned fract) parameters->my_exc.decay);
    log_info("my_exc_init  = %R\n", (unsigned fract) parameters->my_exc.init);
    log_info("my_inh_decay = %R\n", (unsigned fract) parameters->my_inh.decay);
    log_info("my_inh_init  = %R\n", (unsigned fract) parameters->my_inh.init);
    log_info("my_excitatory_value = %11.4k\n",
            parameters->my_exc.synaptic_input_value);
    log_info("my_inhibitory_value = %11.4k\n",
            parameters->my_inh.synaptic_input_value);
}

#endif  // _SYNAPSE_TYPES_MY_IMPL_H_
