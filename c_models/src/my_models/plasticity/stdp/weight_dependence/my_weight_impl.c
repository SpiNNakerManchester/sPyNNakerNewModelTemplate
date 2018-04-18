#include "my_weight_impl.h"

// Global plasticity parameter data
plasticity_weight_region_data_t
    plasticity_weight_region_data[SYNAPSE_TYPE_COUNT];

address_t weight_initialise(
        address_t address, uint32_t *ring_buffer_to_input_buffer_left_shifts) {

    // This can be used to indicate the scaling used on the weights
    use(ring_buffer_to_input_buffer_left_shifts);

    log_info("weight_initialise: starting");
    log_info("\tSTDP my weight dependence");

    // Copy plasticity parameter data from address
    int32_t *plasticity_word = (int32_t*) address;
    for (uint32_t s = 0; s < SYNAPSE_TYPE_COUNT; s++) {
        plasticity_weight_region_data[s].min_weight = *plasticity_word++;
        plasticity_weight_region_data[s].max_weight = *plasticity_word++;
        plasticity_weight_region_data[s].my_parameter = *plasticity_word++;

        // TODO: Copy any other data
    }
    log_info("weight_initialise: completed successfully");

    // Return end address of region
    return (address_t) plasticity_word;
}
