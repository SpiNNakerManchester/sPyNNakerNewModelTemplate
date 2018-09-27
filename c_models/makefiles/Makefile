MODELS = my_model_curr_exp \
    my_model_curr_exp_my_additional_input \
    my_model_curr_exp_my_threshold \
    my_model_curr_exp_my_input_type \
    my_model_curr_my_synapse_type \
    my_model_curr_exp_stdp_mad_my_timing_my_weight \
    my_full_neuron_impl

all:
	for d in $(MODELS); do $(MAKE) -C $$d || exit $$?; done

clean:
	for d in $(MODELS); do $(MAKE) -C $$d clean || exit $$?; done
