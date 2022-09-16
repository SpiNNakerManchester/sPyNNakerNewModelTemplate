#ifndef _MY_INPUT_TYPE_H_
#define _MY_INPUT_TYPE_H_

#include <neuron/input_types/input_type.h>

typedef struct input_type_t {
    REAL multiplicator;
    REAL my_parameter;
} input_type_t;

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
    input_t total = 0.0;
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
