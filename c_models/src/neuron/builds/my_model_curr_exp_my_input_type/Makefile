APP = $(notdir $(CURDIR))
BUILD_DIR = build/

NEURON_MODEL = $(EXTRA_SRC_DIR)/neuron/models/my_neuron_model_impl.c
NEURON_MODEL_H = $(EXTRA_SRC_DIR)/neuron/models/my_neuron_model_impl.h
INPUT_TYPE_H = $(EXTRA_SRC_DIR)/neuron/input_types/my_input_type.h
NEURON_IMPL_H = $(EXTRA_SRC_DIR)/neuron/implementations/my_neuron_impl.h
SYNAPSE_IMPL_H = $(EXTRA_SRC_DIR)/neuron/implementations/my_synapse_impl.h
THRESHOLD_TYPE_H = $(SOURCE_DIR)/neuron/threshold_types/threshold_type_static.h
SYNAPSE_TYPE_H = $(SOURCE_DIR)/neuron/synapse_types/synapse_types_exponential_impl.h
SYNAPSE_DYNAMICS = $(SOURCE_DIR)/neuron/plasticity/synapse_dynamics_static_impl.c

include ../Makefile.common
