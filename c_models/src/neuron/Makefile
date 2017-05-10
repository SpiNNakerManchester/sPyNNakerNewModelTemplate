MODELS = my_model_curr_exp \
    my_model_curr_exp_my_additional_input \
    my_model_curr_exp_my_threshold \
    my_model_curr_exp_stdp_mad_my_timing_my_weight \
    my_model_curr_my_synapse_type

BUILD_DIRS := $(addprefix builds/, $(MODELS))

all: $(BUILD_DIRS)
	for d in $(BUILD_DIRS); do (cd $$d; "$(MAKE)") || exit $$?; done

clean: $(BUILD_DIRS)
	for d in $(BUILD_DIRS); do (cd $$d; "$(MAKE)" clean) || exit $$?; done
