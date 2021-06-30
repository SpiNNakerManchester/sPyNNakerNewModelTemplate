MODELS = my_model_curr_exp \
    my_model_curr_exp_my_additional_input \
    my_model_curr_exp_my_threshold \
    my_model_curr_exp_my_input_type \
    my_model_curr_my_synapse_type \
    my_model_curr_exp_stdp_mad_my_timing_my_weight \
    my_if_curr_exp_sEMD \
    my_full_neuron_impl \
    my_model_curr_exp_neuron \
    my_model_curr_exp_my_additional_input_neuron \
    my_model_curr_exp_my_threshold_neuron \
    my_model_curr_exp_my_input_type_neuron \
    my_model_curr_my_synapse_type_neuron \
    synapses_stdp_mad_my_timing_my_weight \
    my_if_curr_exp_sEMD_neuron \
    my_full_neuron_impl_neuron

all:
	for d in $(MODELS); do $(MAKE) -C $$d || exit $$?; done

clean:
	for d in $(MODELS); do $(MAKE) -C $$d clean || exit $$?; done
