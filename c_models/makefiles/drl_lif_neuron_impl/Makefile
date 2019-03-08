APP = $(notdir $(CURDIR))

CFLAGS += -Wall -Wextra -Ofast -finline-limit=4

NEURON_IMPL_H = $(EXTRA_SRC_DIR)/my_models/implementations/drl_lif_neuron_impl.h
SYNAPSE_DYNAMICS = $(NEURON_DIR)/neuron/plasticity/synapse_dynamics_static_impl.c

include ../extra.mk
