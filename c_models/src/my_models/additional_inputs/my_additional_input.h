#ifndef _MY_ADDITIONAL_INPUT_H_
#define _MY_ADDITIONAL_INPUT_H_

#include <neuron/additional_inputs/additional_input.h>

//! \brief These are the parameters as specified in the Python code
struct additional_input_params_t {
    REAL my_parameter;
    REAL input_current_init;
};

//! \brief These are the parameters used by the C code; these might differ
//!        from the Python input parameters e.g. if there are values computed
//!        for efficiency.
struct additional_input_t {
    REAL my_parameter;
    REAL input_current;
};

//! \brief Set up the state from the parameters
//! \param[out] state The state to write to
//! \param[in] params The parameters to read from
static inline void additional_input_initialise(
        additional_input_t *state, additional_input_params_t *params,
        UNUSED uint32_t n_steps_per_timestep) {
    state->my_parameter = params->my_parameter;
    state->input_current = params->input_current_init;
}

//! \brief Write the state back to the parameters where possible
//! \param[in] state The state to read from
//! \param[out] params The parameters to write to
static inline void additional_input_save_state(additional_input_t *state,
        additional_input_params_t *params) {
    params->input_current_init = state->input_current;
}

//! \brief Gets the value of current provided by the additional input this
//!     timestep
//! \param[in] additional_input The additional input type pointer to the
//!     parameters
//! \param[in] membrane_voltage The membrane voltage of the neuron
//! \return The value of the input after scaling
static input_t additional_input_get_input_value_as_current(
        additional_input_t *additional_input,
        state_t membrane_voltage) {
    use(membrane_voltage);
    additional_input->input_current += additional_input->my_parameter;
    return additional_input->input_current;
}

//! \brief Notifies the additional input type that the neuron has spiked
//! \param[in] additional_input The additional input type pointer to the
//!     parameters
static void additional_input_has_spiked(
        additional_input_t *additional_input) {
    additional_input->input_current = ZERO;
}

#endif // _MY_ADDITIONAL_INPUT_H_
