#ifndef _MY_NEURON_IMPL_INCL_INPUT_AND_THRESHOLD_H_
#define _MY_NEURON_IMPL_INCL_INPUT_AND_THRESHOLD_H_

// Attempting to demonstrate that a "neuron model" can be defined in a different
// way without the use of components for additional input / input / threshold

#include <neuron/implementations/neuron_impl.h>
#include <neuron/models/neuron_model.h>
#include <neuron/synapse_types/synapse_types.h>
#include <neuron/plasticity/synapse_dynamics.h>
#include <common/out_spikes.h>
#include <recording.h>
#include <string.h>

//! neuron_impl_t struct
typedef struct neuron_impl_t {
} neuron_impl_t;

#define SPIKE_RECORDING_CHANNEL 0
#define V_RECORDING_CHANNEL 1
#define GSYN_EXCITATORY_RECORDING_CHANNEL 2
#define GSYN_INHIBITORY_RECORDING_CHANNEL 3

//! Array of neuron states
static neuron_pointer_t neuron_array;

//! Global parameters for the neurons
static global_neuron_params_pointer_t global_parameters;

//! The number of neurons on the core
static uint32_t n_neurons;

//! The recording flags
static uint32_t recording_flags;

// The synapse shaping parameters
static synapse_param_t *neuron_synapse_shaping_params;

//! storage for neuron state with timestamp
static timed_state_t *voltages;
uint32_t voltages_size;

//! storage for neuron input with timestamp
static timed_input_t *inputs_excitatory;
static timed_input_t *inputs_inhibitory;
uint32_t input_size;

//! The number of recordings outstanding
static uint32_t n_recordings_outstanding = 0;

//! \brief Initialise the particular implementation of the data
//! \param[in] data_address The address of the data to be initialised
//! \return boolean for error
static bool neuron_impl_initialise(uint32_t n_neurons)
{
    // log message for debug purposes
    log_info(
        "\t neurons = %u, params size = %u,"
        "input type size = %u, threshold size = %u", n_neurons,
        sizeof(neuron_t), sizeof(input_type_t), sizeof(threshold_type_t));

    // allocate DTCM for the global parameter details
    if (sizeof(global_neuron_params_t) > 0) {
        global_parameters = (global_neuron_params_t *) spin1_malloc(
            sizeof(global_neuron_params_t));
        if (global_parameters == NULL) {
            log_error("Unable to allocate global neuron parameters"
                      "- Out of DTCM");
            return false;
        }
    }

    // Allocate DTCM for neuron array
    if (sizeof(neuron_t) != 0) {
        neuron_array = (neuron_t *) spin1_malloc(n_neurons * sizeof(neuron_t));
        if (neuron_array == NULL) {
            log_error("Unable to allocate neuron array - Out of DTCM");
            return false;
        }
    }

    voltages_size = sizeof(uint32_t) + sizeof(state_t) * n_neurons;
    voltages = (timed_state_t *) spin1_malloc(voltages_size);
    input_size = sizeof(uint32_t) + sizeof(input_struct_t) * n_neurons;
    inputs_excitatory = (timed_input_t *) spin1_malloc(input_size);
    inputs_inhibitory = (timed_input_t *) spin1_malloc(input_size);
}

//! \brief Add inputs as required to the implementation
//! \param[in] weights_this_timestep Weight inputs to be added
//static void neuron_impl_add_inputs(input_t weights_this_timestep[N_RING_BUFFERS]);
//{
//	use(weights_this_timestep);
//}

//! \bried Load in the neuron parameters... ?
//! \return None
static void neuron_impl_load_neuron_parameters(address_t data_address, uint32_t next)
{
    log_info("loading neuron global parameters");
    memcpy(global_parameters, &data_address[next], sizeof(global_neuron_params_t));
    next += sizeof(global_neuron_params_t) / 4;

    log_info("loading neuron local parameters");
    memcpy(neuron_array, &data_address[next], n_neurons * sizeof(neuron_t));
    next += (n_neurons * sizeof(neuron_t)) / 4;
}

//! \brief Wrapper to set global neuron parameters ?
//! \return None
static void neuron_impl_set_global_neuron_parameters()
{
    neuron_model_set_global_neuron_params(global_parameters);
}

//! \brief Do the timestep update for the particular implementation
//! \param[in] neuron index
//! \return bool value for whether a spike has occurred
static bool neuron_impl_do_timestep_update(timer_t time, index_t neuron_index)
{
	// Get the neuron itself
    neuron_pointer_t neuron = &neuron_array[neuron_index];

    // Get the voltage
    state_t voltage = neuron_impl_get_membrane_voltage(neuron_index);

    // If we should be recording potential, record this neuron parameter
    voltages->states[neuron_index] = voltage;

    // Get the exc and inh values from the synapses
    input_t exc_value = synapse_types_get_excitatory_input(
    		&(neuron_synapse_shaping_params[neuron_index]));
    input_t inh_value = synapse_types_get_inhibitory_input(
    		&(neuron_synapse_shaping_params[neuron_index]));

    // Convert exc_input to current here
    input_t exc_input = exc_value * neuron->my_multiplicator;
    input_t inh_input = inh_value + neuron->my_input_parameter;

    // Call functions to get the input values to be recorded
    inputs_excitatory->inputs[neuron_index].input = exc_input;
    inputs_inhibitory->inputs[neuron_index].input = inh_input;

    // Get external bias from any source of intrinsic plasticity
    input_t external_bias =
        synapse_dynamics_get_intrinsic_bias(time, neuron_index);

    // update neuron parameters
    state_t result = neuron_model_state_update(
    		exc_input, inh_input, external_bias, neuron);

    // determine if a spike should occur
    REAL test_value = result * neuron->my_threshold_parameter;

    bool spike = REAL_COMPARE(test_value, >=, neuron->threshold_value);

    // If spike occurs, communicate to relevant parts of model
    if (spike) {
        // Call relevant model-based functions

    	// Tell the neuron model
    	neuron_model_has_spiked(neuron);

        // Do any required synapse processing
        synapse_dynamics_process_post_synaptic_event(time, neuron_index);

        // Record the spike
        out_spikes_set_spike(neuron_index);
    }

    // Return the boolean to the model timestep update
    return spike;
}

//! \setter for the internal input buffers
//! \param[in] input_buffers_value the new input buffers
static void neuron_impl_set_neuron_synapse_shaping_params(
		synapse_param_t *neuron_synapse_shaping_params_value)
{
    neuron_synapse_shaping_params = neuron_synapse_shaping_params_value;
}

//! \brief Wrapper for the neuron model's print state variables function
static void neuron_impl_print_state_variables(index_t neuron_index)
{
	neuron_model_print_state_variables(&(neuron_array[neuron_index]));
}

//! \brief Wrapper for the neuron model's print parameters function
static void neuron_impl_print_parameters(index_t neuron_index)
{
	neuron_model_print_parameters(&(neuron_array[neuron_index]));
}

//! \brief does this work here?
void recording_done_callback() {
    n_recordings_outstanding -= 1;
}

//! \brief Do any required recording
//! \param[in] recording_flags
//! \return None
static void neuron_impl_do_recording(timer_t time, uint32_t recording_flags)
{
	// record neuron state (membrane potential) if needed
	if (recording_is_channel_enabled(recording_flags, V_RECORDING_CHANNEL)) {
		n_recordings_outstanding += 1;
		voltages->time = time;
		recording_record_and_notify(
				V_RECORDING_CHANNEL, voltages, voltages_size,
				recording_done_callback);
	}

	// record neuron inputs (excitatory) if needed
	if (recording_is_channel_enabled(
			recording_flags, GSYN_EXCITATORY_RECORDING_CHANNEL)) {
		n_recordings_outstanding += 1;
		inputs_excitatory->time = time;
		recording_record_and_notify(
				GSYN_EXCITATORY_RECORDING_CHANNEL, inputs_excitatory, input_size,
				recording_done_callback);
	}

	// record neuron inputs (inhibitory) if needed
	if (recording_is_channel_enabled(
			recording_flags, GSYN_INHIBITORY_RECORDING_CHANNEL)) {
		n_recordings_outstanding += 1;
		inputs_inhibitory->time = time;
		recording_record_and_notify(
				GSYN_INHIBITORY_RECORDING_CHANNEL, inputs_inhibitory, input_size,
				recording_done_callback);
	}

	// Record any spikes this timestep
	if (recording_is_channel_enabled(
			recording_flags, SPIKE_RECORDING_CHANNEL)) {
		if (!out_spikes_is_empty()) {
			n_recordings_outstanding += 1;
			out_spikes_record(
					SPIKE_RECORDING_CHANNEL, time, recording_done_callback);
		}
	}
}

//! \return The membrane voltage value
static input_t neuron_impl_get_membrane_voltage(index_t neuron_index)
{
    neuron_pointer_t neuron = &neuron_array[neuron_index];
	return neuron_model_get_membrane_voltage(neuron);
}

#endif // _MY_NEURON_IMPL_INCL_INPUT_AND_THRESHOLD_H_
