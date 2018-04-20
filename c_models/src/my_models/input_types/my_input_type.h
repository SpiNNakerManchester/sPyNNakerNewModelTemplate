#ifndef _MY_INPUT_TYPE_H_
#define _MY_INPUT_TYPE_H_

#ifndef NUM_EXCITATORY_RECEPTORS
#define NUM_EXCITATORY_RECEPTORS 1
#error NUM_EXCITATORY_RECEPTORS was undefined.  It should be defined by a synapse\
       shaping include
#endif

#ifndef NUM_INHIBITORY_RECEPTORS
#define NUM_INHIBITORY_RECEPTORS 1
#error NUM_INHIBITORY_RECEPTORS was undefined.  It should be defined by a synapse\
       shaping include
#endif

#include <neuron/input_types/input_type.h>

typedef struct input_type_t {

    REAL my_multiplicator[NUM_INHIBITORY_RECEPTORS];

    REAL my_input_parameter[NUM_INHIBITORY_RECEPTORS];

} input_type_t;

//! \brief Gets the input value
//! \param[in] value The value to be transformed
//! \param[in] input_type The input type pointer to the parameters
//! \return The input value
static inline input_t* input_type_get_input_value(
        input_t* value, input_type_pointer_t input_type, uint16_t num_receptors) {
    use(input_type);
    for (int i=0; i< num_receptors; i++){
    	value[i] = value[i];  // NOTE: this will be edited in future to be
    	                      //       multiplied by a scaling factor
    }
    return &value[0];
}

//! \brief Set the inhibitory multiplicator value
//! \param[in] value The value to be set
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] inh_input The inhibitory input value
//! \return None
static void input_type_set_inhibitory_multiplicator_value(
		input_t* value, input_type_pointer_t input_type, input_t* inh_input) {

    for (int i=0; i<NUM_INHIBITORY_RECEPTORS; i++){
		if (inh_input[i] >= 0.01 && input_type->my_multiplicator[i]==0 &&
				input_type->my_input_parameter[i] == 0)
		{ input_type->my_multiplicator[i] = value[i]; }
		else if (inh_input[i] < 0.01)
		{ input_type->my_multiplicator[i] = 0; }

		input_type->my_input_parameter[i] = inh_input[i];
    }

}

//! \brief Convert excitatory input to current
//! \param[in] exc_input The excitatory value to be converted
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] membrane_voltage The voltage to use in conversion
//! \return The converted excitatory input
static inline void input_type_convert_excitatory_input_to_current(
        input_t* exc_input, input_type_pointer_t input_type,
        state_t membrane_voltage) {
    use(input_type);
    use(membrane_voltage);
    use(exc_input);
}

//! \brief Convert inhibitory input to current
//! \param[in] inh_input The inhibitory value to be converted
//! \param[in] input_type The input type pointer to the parameters
//! \param[in] membrane_voltage The voltage to use in conversion
//! \return The converted inhibitory input
static inline void input_type_convert_inhibitory_input_to_current(
        input_t* inh_input, input_type_pointer_t input_type,
        state_t membrane_voltage) {
    use(membrane_voltage);

    // This changes inhibitory to excitatory input
    for (int i=0; i<NUM_INHIBITORY_RECEPTORS; i++){
    	inh_input[i] = (
    			-inh_input[i] * input_type->my_multiplicator[i]);
    }
}

#endif // _MY_INPUT_TYPE_H_
