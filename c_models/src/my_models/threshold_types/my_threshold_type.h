#ifndef _ADAP_THRESHOLD_TYPE_H_
#define _ADAP_THRESHOLD_TYPE_H_

#include <neuron/threshold_types/threshold_type.h>

// Adaptive down here
#include <random.h>
//

typedef struct threshold_type_t {
    // TODO: Add any additional parameters here
    REAL threshold_value;
    // REAL my_param;
    //uint32_t prob;
    //uint32_t seed[4];
    REAL tau_theta;
    REAL theta;
} threshold_type_t;

static inline bool threshold_type_is_above_threshold(state_t value,
        threshold_type_t *threshold_type) {

    // TODO: Perform the appropriate operations
    // REAL test_value = value * threshold_type->my_param;
    threshold_type->theta = (threshold_type->theta) * (threshold_type->tau_theta);
    if (REAL_COMPARE(value, >=, (threshold_type->threshold_value) + (threshold_type->theta) - 20) ){
       threshold_type->theta += 2.0;
       return 1;
    }
    // TODO: Update to return true or false depending on if the
    // threshold has been reached
    // return REAL_COMPARE(test_value, >=, threshold_type->threshold_value);
    else {
      return 0;
    }
    // return REAL_COMPARE(Random_num, <, threshold_type->prob);
}

#endif // _ADAP_THRESHOLD_TYPE_H_
