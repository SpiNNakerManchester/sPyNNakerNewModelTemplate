#ifndef _NEURON_MODEL_GLIF3_IMPL_H_
#define _NEURON_MODEL_GLIF3_IMPL_H_

#include <neuron/models/neuron_model.h>
#include <debug.h>

/**
 * GLIF3 (Generalized Leaky Integrate-and-Fire) Neuron Model
 * This model includes after-spike currents with exponential decay.
 *
 * Model equations:
 * dV/dt = (1/C_m) * [I_e + I_asc_0 + I_asc_1 - g*(V - E_L)]
 * dI_asc_j/dt = -k_j * I_asc_j, for j = 0, 1
 *
 * When V >= V_thresh, spike and reset:
 * - V -> V_reset
 * - I_asc_j -> I_asc_j * exp(-k_j * t_ref) + asc_amp_j
 */

// Neuron parameters structure - must match Python model exactly
struct neuron_params_t {
    // State variables (initial values)
    REAL V_init;              // Initial membrane voltage (mV)
    REAL I_asc_0_init;        // Initial after-spike current 0 (nA)
    REAL I_asc_1_init;        // Initial after-spike current 1 (nA)

    // Model parameters
    REAL C_m;                 // Membrane capacitance (nF)
    REAL E_L;                 // Resting potential (mV)
    REAL V_reset;             // Reset voltage (mV)
    REAL V_thresh;            // Threshold voltage (mV)
    REAL asc_amp_0;           // After-spike current amplitude 0 (nA)
    REAL asc_amp_1;           // After-spike current amplitude 1 (nA)
    REAL g;                   // Conductance (uS)
    REAL k0;                  // ASC decay rate 0 (1/ms)
    REAL k1;                  // ASC decay rate 1 (1/ms)
    REAL t_ref;               // Refractory period (ms)
    REAL I_offset;            // Offset current (nA)
};

// Neuron state structure
struct neuron_t {
    // State variables
    REAL V;                   // Membrane voltage (mV)
    REAL I_asc_0;             // After-spike current 0 (nA)
    REAL I_asc_1;             // After-spike current 1 (nA)

    // Model parameters (copied for efficiency)
    REAL C_m;                 // Membrane capacitance (nF)
    REAL E_L;                 // Resting potential (mV)
    REAL V_reset;             // Reset voltage (mV)
    REAL V_thresh;            // Threshold voltage (mV)
    REAL asc_amp_0;           // After-spike current amplitude 0 (nA)
    REAL asc_amp_1;           // After-spike current amplitude 1 (nA)
    REAL g;                   // Conductance (uS)
    REAL k0;                  // ASC decay rate 0 (1/ms)
    REAL k1;                  // ASC decay rate 1 (1/ms)
    REAL t_ref;               // Refractory period (ms)
    REAL I_offset;            // Offset current (nA)

    // Precomputed values for efficiency
    REAL exp_k0_dt;           // exp(-k0 * dt)
    REAL exp_k1_dt;           // exp(-k1 * dt)
    REAL exp_k0_tref;         // exp(-k0 * t_ref)
    REAL exp_k1_tref;         // exp(-k1 * t_ref)
    REAL dt_over_cm;          // dt / C_m
    REAL g_dt_over_cm;        // g * dt / C_m

    // Refractory period tracking
    uint32_t refract_timer;   // Refractory period timer (in time steps)
    uint32_t refract_steps;   // Total refractory period (in time steps)
};

static inline void neuron_model_initialise(neuron_t *state, neuron_params_t *params,
        uint32_t n_steps_per_timestep) {

    // Initialize state variables
    state->V = params->V_init;
    state->I_asc_0 = params->I_asc_0_init;
    state->I_asc_1 = params->I_asc_1_init;

    // Copy parameters
    state->C_m = params->C_m;
    state->E_L = params->E_L;
    state->V_reset = params->V_reset;
    state->V_thresh = params->V_thresh;
    state->asc_amp_0 = params->asc_amp_0;
    state->asc_amp_1 = params->asc_amp_1;
    state->g = params->g;
    state->k0 = params->k0;
    state->k1 = params->k1;
    state->t_ref = params->t_ref;
    state->I_offset = params->I_offset;

    // Precompute exponentials and other constants for efficiency
    // dt is the simulation timestep in milliseconds
    REAL dt = KDIVUI(1, n_steps_per_timestep);

    state->exp_k0_dt = EXPK(-state->k0 * dt);
    state->exp_k1_dt = EXPK(-state->k1 * dt);
    state->exp_k0_tref = EXPK(-state->k0 * state->t_ref);
    state->exp_k1_tref = EXPK(-state->k1 * state->t_ref);
    state->dt_over_cm = dt / state->C_m;
    state->g_dt_over_cm = state->g * dt / state->C_m;

    // Calculate refractory period in time steps
    state->refract_steps = (uint32_t) (state->t_ref * n_steps_per_timestep);
    state->refract_timer = 0;
}

static inline void neuron_model_save_state(neuron_t *state, neuron_params_t *params) {
    // Save state variables for continuation in next run
    params->V_init = state->V;
    params->I_asc_0_init = state->I_asc_0;
    params->I_asc_1_init = state->I_asc_1;
}

static state_t neuron_model_state_update(
        uint16_t num_excitatory_inputs, const input_t* exc_input,
        uint16_t num_inhibitory_inputs, const input_t* inh_input,
        input_t external_bias, REAL current_offset, neuron_t *restrict neuron) {

    // If in refractory period, just decrement timer and return current voltage
    if (neuron->refract_timer > 0) {
        neuron->refract_timer--;
        return neuron->V;
    }

    // Sum excitatory and inhibitory inputs
    REAL total_exc = ZERO;
    REAL total_inh = ZERO;
    for (uint32_t i = 0; i < num_excitatory_inputs; i++) {
        total_exc += exc_input[i];
    }
    for (uint32_t i = 0; i < num_inhibitory_inputs; i++) {
        total_inh += inh_input[i];
    }

    // Total input current
    REAL I_total = total_exc - total_inh + external_bias + neuron->I_offset + current_offset;

    // Update after-spike currents (exponential decay)
    neuron->I_asc_0 *= neuron->exp_k0_dt;
    neuron->I_asc_1 *= neuron->exp_k1_dt;

    // Add after-spike currents to total current
    I_total += neuron->I_asc_0 + neuron->I_asc_1;

    // Update membrane voltage
    // dV/dt = (1/C_m) * [I_total - g*(V - E_L)]
    // V(t+dt) = V(t) + (dt/C_m) * [I_total - g*(V(t) - E_L)]
    REAL leak_current = neuron->g * (neuron->V - neuron->E_L);
    neuron->V += neuron->dt_over_cm * (I_total - leak_current);

    // Return voltage for threshold comparison
    return neuron->V;
}

static state_t neuron_model_get_membrane_voltage(const neuron_t *neuron) {
    return neuron->V;
}

static void neuron_model_has_spiked(neuron_t *restrict neuron) {
    // Reset voltage
    neuron->V = neuron->V_reset;

    // Update after-spike currents
    // I_asc_j(t+) = I_asc_j(t-) * exp(-k_j * t_ref) + asc_amp_j
    neuron->I_asc_0 = neuron->I_asc_0 * neuron->exp_k0_tref + neuron->asc_amp_0;
    neuron->I_asc_1 = neuron->I_asc_1 * neuron->exp_k1_tref + neuron->asc_amp_1;

    // Start refractory period
    neuron->refract_timer = neuron->refract_steps;
}

static inline void neuron_model_print_state_variables(const neuron_t *neuron) {
    log_info("V = %11.4k mV", neuron->V);
    log_info("I_asc_0 = %11.4k nA", neuron->I_asc_0);
    log_info("I_asc_1 = %11.4k nA", neuron->I_asc_1);
    log_info("Refract timer = %u", neuron->refract_timer);
}

static inline void neuron_model_print_parameters(const neuron_t *neuron) {
    log_info("C_m = %11.4k nF", neuron->C_m);
    log_info("E_L = %11.4k mV", neuron->E_L);
    log_info("V_reset = %11.4k mV", neuron->V_reset);
    log_info("V_thresh = %11.4k mV", neuron->V_thresh);
    log_info("asc_amp_0 = %11.4k nA", neuron->asc_amp_0);
    log_info("asc_amp_1 = %11.4k nA", neuron->asc_amp_1);
    log_info("g = %11.4k uS", neuron->g);
    log_info("k0 = %11.4k 1/ms", neuron->k0);
    log_info("k1 = %11.4k 1/ms", neuron->k1);
    log_info("t_ref = %11.4k ms", neuron->t_ref);
    log_info("I_offset = %11.4k nA", neuron->I_offset);
}

#endif // _NEURON_MODEL_GLIF3_IMPL_H_
