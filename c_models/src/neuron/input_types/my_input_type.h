#ifndef _MY_INPUT_TYPE_H_
#define _MY_INPUT_TYPE_H_

#include <neuron/input_types/input_type.h>

typedef struct input_type_t {

    REAL my_multiplicator;

    REAL my_input_parameter;

} input_type_t;

//! \brief Gets the input value
//! \param[in] value The value to be transformed
//! \param[in] input_type The input type pointer to the parameters
//! \return The input value
static inline input_t input_type_get_input_value(
        input_t value, input_type_pointer_t input_type) {
    use(input_type);
    return value;
}

//! \brief Set the inhibitory multiplicator value
//! \param[in] value The value to be set
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] inh_input The inhibitory input value
//! \return None
static void input_type_set_inhibitory_multiplicator_value(
		input_t value, input_type_pointer_t input_type,
		input_t inh_input) {
	if (inh_input >= 0.01 && input_type->my_multiplicator==0 &&
			input_type->my_input_parameter == 0)
	{ input_type->my_multiplicator = value; }
	else if (inh_input < 0.01)
	{ input_type->my_multiplicator = 0; }

	input_type->my_input_parameter = inh_input;
}

//! \brief Convert excitatory input to current
//! \param[in] exc_input The excitatory value to be converted
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] membrane_voltage The voltage to use in conversion
//! \return The converted excitatory input
static inline input_t input_type_convert_excitatory_input_to_current(
        input_t exc_input, input_type_pointer_t input_type,
        state_t membrane_voltage) {
    use(input_type);
    use(membrane_voltage);
    return exc_input;
}

//! \brief Convert inhibitory input to current
//! \param[in] inh_input The inhibitory value to be converted
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] membrane_voltage The voltage to use in conversion
//! \return The converted inhibitory input
static inline input_t input_type_convert_inhibitory_input_to_current(
        input_t inh_input, input_type_pointer_t input_type,
        state_t membrane_voltage) {
    use(membrane_voltage);

    // This changes inhibitory to excitatory input
    // (without the multiplication factor of 40 used in sEMD model, to test...)
    return (-inh_input * input_type->my_multiplicator);
}

#endif // _MY_INPUT_TYPE_H_
