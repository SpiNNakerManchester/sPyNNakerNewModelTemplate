APP = $(notdir $(CURDIR))
BUILD_DIR = build/

NEURON_IMPL_H = $(NEURON_DIR)/neuron/implementations/neuron_impl_standard.h
NEURON_MODEL = $(EXTRA_SRC_DIR)/my_models/models/my_neuron_model_impl.c
NEURON_MODEL_H = $(EXTRA_SRC_DIR)/my_models/models/my_neuron_model_impl.h
INPUT_TYPE_H = $(NEURON_DIR)/neuron/input_types/input_type_current.h
THRESHOLD_TYPE_H = $(NEURON_DIR)/neuron/threshold_types/threshold_type_static.h
SYNAPSE_TYPE_H = $(NEURON_DIR)/neuron/synapse_types/synapse_types_exponential_impl.h
SYNAPSE_DYNAMICS = $(NEURON_DIR)/neuron/plasticity/stdp/synapse_dynamics_stdp_mad_impl.c
TIMING_DEPENDENCE = $(EXTRA_SRC_DIR)/my_models/plasticity/stdp/timing_dependence/my_timing_impl.c
TIMING_DEPENDENCE_H = $(EXTRA_SRC_DIR)/my_models/plasticity/stdp/timing_dependence/my_timing_impl.h
WEIGHT_DEPENDENCE = $(EXTRA_SRC_DIR)/my_models/plasticity/stdp/weight_dependence/my_weight_impl.c
WEIGHT_DEPENDENCE_H = $(EXTRA_SRC_DIR)/my_models/plasticity/stdp/weight_dependence/my_weight_impl.h

include ../extra.mk
