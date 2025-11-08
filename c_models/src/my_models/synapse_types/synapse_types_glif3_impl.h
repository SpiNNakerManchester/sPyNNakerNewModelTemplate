/*! \file
 * \brief GLIF3 synapse type implementation with 4 independent receptors
 *
 * \details This implements 4 independent exponential synapses for the GLIF3 model,
 * allowing different time constants for each receptor type.
 */

#ifndef _SYNAPSE_TYPES_GLIF3_IMPL_H_
#define _SYNAPSE_TYPES_GLIF3_IMPL_H_

#include <neuron/synapse_types/exp_synapse_utils.h>
#include <debug.h>

// 4 synapse types require 2 bits (2^2 = 4)
#define SYNAPSE_TYPE_BITS 2

// 4 synapse types for GLIF3 (tau_syn0, tau_syn1, tau_syn2, tau_syn3)
#define SYNAPSE_TYPE_COUNT 4

// Parameters for 4 independent exponential synapses
struct synapse_types_params_t {
    exp_params_t syn_0;  // tau_syn0
    exp_params_t syn_1;  // tau_syn1
    exp_params_t syn_2;  // tau_syn2
    exp_params_t syn_3;  // tau_syn3
    REAL time_step_ms;
};

// State for 4 independent exponential synapses
struct synapse_types_t {
    exp_state_t syn_0;  // tau_syn0
    exp_state_t syn_1;  // tau_syn1
    exp_state_t syn_2;  // tau_syn2
    exp_state_t syn_3;  // tau_syn3
};

// All 4 receptors are excitatory (can be made inhibitory by connection weight sign)
#define NUM_EXCITATORY_RECEPTORS 4
#define NUM_INHIBITORY_RECEPTORS 0

// Include this after defining the above
#include <neuron/synapse_types/synapse_types.h>

// Synapse type indices
typedef enum input_buffer_regions {
    SYNAPSE_0, SYNAPSE_1, SYNAPSE_2, SYNAPSE_3
} input_buffer_regions;

static inline void synapse_types_initialise(synapse_types_t *state,
        synapse_types_params_t *params, uint32_t n_steps_per_timestep) {
    decay_and_init(&state->syn_0, &params->syn_0, params->time_step_ms, n_steps_per_timestep);
    decay_and_init(&state->syn_1, &params->syn_1, params->time_step_ms, n_steps_per_timestep);
    decay_and_init(&state->syn_2, &params->syn_2, params->time_step_ms, n_steps_per_timestep);
    decay_and_init(&state->syn_3, &params->syn_3, params->time_step_ms, n_steps_per_timestep);
}

static inline void synapse_types_save_state(synapse_types_t *state,
        synapse_types_params_t *params) {
    params->syn_0.init_input = state->syn_0.synaptic_input_value;
    params->syn_1.init_input = state->syn_1.synaptic_input_value;
    params->syn_2.init_input = state->syn_2.synaptic_input_value;
    params->syn_3.init_input = state->syn_3.synaptic_input_value;
}

//! \brief Shapes the synaptic input (exponential decay)
static inline void synapse_types_shape_input(synapse_types_t *parameters) {
    exp_shaping(&parameters->syn_0);
    exp_shaping(&parameters->syn_1);
    exp_shaping(&parameters->syn_2);
    exp_shaping(&parameters->syn_3);
}

//! \brief Adds input to the appropriate synapse type
static inline void synapse_types_add_neuron_input(
        index_t synapse_type_index, synapse_types_t *parameters,
        input_t input) {
    switch (synapse_type_index) {
        case SYNAPSE_0:
            add_input_exp(&parameters->syn_0, input);
            break;
        case SYNAPSE_1:
            add_input_exp(&parameters->syn_1, input);
            break;
        case SYNAPSE_2:
            add_input_exp(&parameters->syn_2, input);
            break;
        case SYNAPSE_3:
            add_input_exp(&parameters->syn_3, input);
            break;
        default:
            log_error("Invalid synapse type index: %d", synapse_type_index);
            break;
    }
}

//! \brief Gets all 4 excitatory inputs
static inline input_t* synapse_types_get_excitatory_input(
        input_t *excitatory_response, synapse_types_t *parameters) {
    excitatory_response[0] = parameters->syn_0.synaptic_input_value;
    excitatory_response[1] = parameters->syn_1.synaptic_input_value;
    excitatory_response[2] = parameters->syn_2.synaptic_input_value;
    excitatory_response[3] = parameters->syn_3.synaptic_input_value;
    return &excitatory_response[0];
}

//! \brief No inhibitory inputs (returns NULL)
static inline input_t* synapse_types_get_inhibitory_input(
        input_t *inhibitory_response, synapse_types_t *parameters) {
    use(inhibitory_response);
    use(parameters);
    return NULL;
}

//! \brief Returns character for synapse type (for debug)
static inline const char *synapse_types_get_type_char(
        index_t synapse_type_index) {
    switch (synapse_type_index) {
        case SYNAPSE_0:
            return "0";
        case SYNAPSE_1:
            return "1";
        case SYNAPSE_2:
            return "2";
        case SYNAPSE_3:
            return "3";
        default:
            log_debug("Did not recognise synapse type %i", synapse_type_index);
            return "?";
    }
}

//! \brief Prints input for debug purposes
static inline void synapse_types_print_input(synapse_types_t *parameters) {
    io_printf(IO_BUF, "%12.6k - %12.6k - %12.6k - %12.6k",
            parameters->syn_0.synaptic_input_value,
            parameters->syn_1.synaptic_input_value,
            parameters->syn_2.synaptic_input_value,
            parameters->syn_3.synaptic_input_value);
}

//! \brief Prints parameters for debug purposes
static inline void synapse_types_print_parameters(synapse_types_t *parameters) {
    log_info("syn_0_decay = %R\n", (unsigned fract) parameters->syn_0.decay);
    log_info("syn_0_init  = %R\n", (unsigned fract) parameters->syn_0.init);
    log_info("syn_0_value = %11.4k\n", parameters->syn_0.synaptic_input_value);

    log_info("syn_1_decay = %R\n", (unsigned fract) parameters->syn_1.decay);
    log_info("syn_1_init  = %R\n", (unsigned fract) parameters->syn_1.init);
    log_info("syn_1_value = %11.4k\n", parameters->syn_1.synaptic_input_value);

    log_info("syn_2_decay = %R\n", (unsigned fract) parameters->syn_2.decay);
    log_info("syn_2_init  = %R\n", (unsigned fract) parameters->syn_2.init);
    log_info("syn_2_value = %11.4k\n", parameters->syn_2.synaptic_input_value);

    log_info("syn_3_decay = %R\n", (unsigned fract) parameters->syn_3.decay);
    log_info("syn_3_init  = %R\n", (unsigned fract) parameters->syn_3.init);
    log_info("syn_3_value = %11.4k\n", parameters->syn_3.synaptic_input_value);
}

#endif  // _SYNAPSE_TYPES_GLIF3_IMPL_H_
