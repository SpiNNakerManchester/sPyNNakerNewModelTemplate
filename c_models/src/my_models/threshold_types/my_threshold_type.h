#ifndef _MY_THRESHOLD_TYPE_H_
#define _MY_THRESHOLD_TYPE_H_

#include <neuron/threshold_types/threshold_type.h>

struct threshold_type_params_t {
    // TODO: Add any additional parameters here
    REAL threshold_value;
    REAL my_param;
};

struct threshold_type_t {
    // TODO: Add any additional state here
    REAL threshold_value;
    REAL my_param;
};

static inline void threshold_type_initialise(threshold_type_t *state,
        threshold_type_params_t *params, UNUSED uint32_t n_steps_per_timestep) {
    state->threshold_value = params->threshold_value;
    state->my_param = params->my_param;
}

static inline void threshold_type_save_state(UNUSED threshold_type_t *state,
        UNUSED threshold_type_params_t * params) {
    // Unused because nothing changes during run
}

static inline bool threshold_type_is_above_threshold(state_t value,
        threshold_type_t *threshold_type) {

    // TODO: Perform the appropriate operations
    REAL test_value = value * threshold_type->my_param;

    // TODO: Update to return true or false depending on if the
    // threshold has been reached
    return REAL_COMPARE(test_value, >=, threshold_type->threshold_value);
}

#endif // _MY_THRESHOLD_TYPE_H_
