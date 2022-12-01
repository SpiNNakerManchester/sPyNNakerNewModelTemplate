#ifndef _NEURON_MODEL_MY_IMPL_H_
#define _NEURON_MODEL_MY_IMPL_H_

#include <neuron/models/neuron_model.h>

struct neuron_params_t {
    // TODO: Parameters - make sure these match with the Python code,
    // including the order of the variables

    // Variable-state parameters e.g. membrane voltage
    REAL V_init;
    // offset current [nA]
    REAL I_offset;
    // Put anything else you want to store per neuron
    REAL my_parameter;
};

struct neuron_t {
    // TODO: State.  This might match with the above parameters, but can also
    // differ if some calculations are made on the parameters during initialization
    // for efficiency

    // Variable-state parameters e.g. membrane voltage
    REAL V;
    // offset current [nA]
    REAL I_offset;
    // Put anything else you want to store per neuron
    REAL my_parameter;
};

static inline void neuron_model_initialise(neuron_t *state, neuron_params_t *params,
        UNUSED uint32_t n_steps_per_timestep) {
    // TODO: Make sure state variables are all set up
    state->V = params->V_init;
    state->I_offset = params->I_offset;
    state->my_parameter = params->my_parameter;
}

static inline void neuron_model_save_state(neuron_t *state, neuron_params_t *params) {
    // TODO: Copy back anything that changes during the run so that the state
    // continues in the next run
    params->V_init = state->V;
}

static state_t neuron_model_state_update(
        uint16_t num_excitatory_inputs, const input_t* exc_input,
        uint16_t num_inhibitory_inputs, const input_t* inh_input,
        input_t external_bias, REAL current_offset, neuron_t *restrict neuron) {

    // This takes the input and generates an input value, assumed to be a
    // current.  Note that the conversion to current from conductance is done
    // outside of this function, so does not need to be repeated here.

    // Sum contributions from multiple inputs (if used)
    REAL total_exc = ZERO;
    REAL total_inh = ZERO;
    for (uint32_t i = 0; i < num_excitatory_inputs; i++) {
        total_exc += exc_input[i];
    }
    for (uint32_t i = 0; i < num_inhibitory_inputs; i++) {
        total_inh += inh_input[i];
    }

    input_t input_this_timestep =
            total_exc - total_inh + external_bias + neuron->I_offset + current_offset;

    // TODO: Solve your equation here
    neuron->V += input_this_timestep;

    // Return the state variable to be compared with the threshold value
    // to determine if the neuron has spikes (commonly the membrane voltage)
    // TODO: Update to return the correct variable
    return neuron->V;
}

static state_t neuron_model_get_membrane_voltage(const neuron_t *neuron) {

    // TODO: Get the state value representing the membrane voltage
    return neuron->V;
}

static void neuron_model_has_spiked(neuron_t *restrict neuron) {

    // TODO: Perform operations required to reset the state after a spike
    neuron->V = neuron->my_parameter;
}

static inline void neuron_model_print_state_variables(const neuron_t *neuron) {

    // TODO: Print all state variables
    log_info("V = %11.4k mv", neuron->V);
}

static inline void neuron_model_print_parameters(const neuron_t *neuron) {

    // TODO: Print all neuron parameters
    log_info("my parameter = %11.4k mv", neuron->my_parameter);
}

#endif // _NEURON_MODEL_MY_IMPL_H_
