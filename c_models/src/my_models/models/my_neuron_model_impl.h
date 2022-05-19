#ifndef _NEURON_MODEL_MY_IMPL_H_
#define _NEURON_MODEL_MY_IMPL_H_

#include <neuron/models/neuron_model.h>

typedef struct neuron_t {
    // TODO: Parameters - make sure these match with the Python code,
    // including the order of the variables when returned by
    // get_neural_parameters.

    // Variable-state parameters e.g. membrane voltage
    REAL V;
    // offset current [nA]
    REAL I_offset;
    // Put anything else you want to store per neuron
    REAL my_parameter;
} neuron_t;

typedef struct global_neuron_params_t {
    // TODO: Add any parameters that apply to the whole model here (i.e. not
    // just to a single neuron)

    // Note: often these are not user supplied, but computed parameters

    uint32_t machine_time_step;
} global_neuron_params_t;

extern const global_neuron_params_t *global_params;

static state_t neuron_model_state_update(
        uint16_t num_excitatory_inputs, const input_t* exc_input,
        uint16_t num_inhibitory_inputs, const input_t* inh_input,
        input_t external_bias, REAL current_offset, neuron_t *restrict neuron) {

    // This takes the input and generates an input value, assumed to be a
    // current.  Note that the conversion to current from conductance is done
    // outside of this function, so does not need to be repeated here.

    // Sum contributions from multiple inputs (if used)
    REAL total_exc = 0;
    REAL total_inh = 0;
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

#endif // _NEURON_MODEL_MY_IMPL_H_
