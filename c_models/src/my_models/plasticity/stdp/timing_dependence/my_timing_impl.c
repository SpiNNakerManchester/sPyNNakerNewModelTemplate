#include "my_timing_impl.h"

// TODO: Set up any variables here
accum my_potentiation_parameter;
accum my_depression_parameter;

//---------------------------------------
// Functions
//---------------------------------------
address_t timing_initialise(address_t address) {

    log_info("timing_initialise: starting");
    log_info("\tSTDP my timing rule");

    // TODO: copy parameters from memory
    spin1_memcpy(&my_potentiation_parameter, &(address[0]), 4);
    spin1_memcpy(&my_depression_parameter, &(address[1]), 4);

    log_info("my potentiation parameter = %k", my_potentiation_parameter);
    log_info("my depression parameter = %k", my_depression_parameter);
    log_info("timing_initialise: completed successfully");

    // TODO: Return the address after the last one read
    return &(address[2]);
}
