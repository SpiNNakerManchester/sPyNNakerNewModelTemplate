APP = $(notdir $(CURDIR))
BUILD_DIR = build/

NEURON_IMPL_H = $(NEURON_DIR)/neuron/implementations/neuron_impl_standard.h
NEURON_MODEL = $(EXTRA_SRC_DIR)/my_models/models/my_neuron_model_impl.c
NEURON_MODEL_H = $(EXTRA_SRC_DIR)/my_models/models/my_neuron_model_impl.h
ADDITIONAL_INPUT_H = $(EXTRA_SRC_DIR)/my_models/additional_inputs/my_additional_input.h
INPUT_TYPE_H = $(NEURON_DIR)/neuron/input_types/input_type_current.h
THRESHOLD_TYPE_H = $(NEURON_DIR)/neuron/threshold_types/threshold_type_static.h
SYNAPSE_TYPE_H = $(NEURON_DIR)/neuron/synapse_types/synapse_types_exponential_impl.h

include ../extra_neuron.mk
