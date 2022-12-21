#ifndef _MY_INPUT_TYPE_H_
#define _MY_INPUT_TYPE_H_

#include <neuron/input_types/input_type.h>

//! \brief These are the parameters as specified in the Python code
struct input_type_params_t {
    REAL multiplicator_init;
    REAL my_parameter;
};

//! \brief These are the parameters used by the C code; these might differ
//!        from the Python input parameters e.g. if there are values computed
//!        for efficiency.
struct input_type_t {
    REAL multiplicator;
    REAL my_parameter;
};

//! \brief Set up the state from the parameters
//! \param[out] state The state to write to
//! \param[in] params The parameters to read from
static inline void input_type_initialise(
        input_type_t *state, input_type_params_t *params,
        UNUSED uint32_t n_steps_per_timestep) {
    state->my_parameter = params->my_parameter;
    state->multiplicator = params->multiplicator_init;
}

//! \brief Write the state back to the parameters where possible
//! \param[in] state The state to read from
//! \param[out] params The parameters to write to
static inline void input_type_save_state(input_type_t *state,
        input_type_params_t *params) {
    params->multiplicator_init = state->multiplicator;
}

static inline void input_type_set_multiplicator_value(
        input_t total, input_type_t *input_type) {
    if (total > input_type->my_parameter) {
        input_type->multiplicator = 1.0k;
    } else {
        input_type->multiplicator += 1.0k;
    }
}

static inline input_t *input_type_get_input_value(
        input_t *restrict value, input_type_t *input_type,
        uint16_t num_receptors) {
    input_t total = ZERO;
    for (int i = 0; i < num_receptors; i++) {
        total += value[i];
    }

    input_type_set_multiplicator_value(total, input_type);

    return &value[0];
}

static inline void input_type_convert_excitatory_input_to_current(
        input_t *restrict exc_input, const input_type_t *input_type,
        state_t membrane_voltage) {
    use(membrane_voltage);

    for (int i=0; i < NUM_EXCITATORY_RECEPTORS; i++) {
        exc_input[i] = exc_input[i] * input_type->multiplicator;
    }
}

static inline void input_type_convert_inhibitory_input_to_current(
        input_t *restrict inh_input, const input_type_t *input_type,
        state_t membrane_voltage) {
    use(membrane_voltage);

    for (int i=0; i < NUM_INHIBITORY_RECEPTORS; i++) {
        inh_input[i] = inh_input[i] * input_type->multiplicator;
    }
}

#endif // _MY_INPUT_TYPE_H_
