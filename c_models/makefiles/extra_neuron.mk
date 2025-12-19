CUR_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/)
SPYNNAKER_INSTALL_DIR := $(strip $(if $(SPYNNAKER_INSTALL_DIR), $(SPYNNAKER_INSTALL_DIR), $(abspath $(CUR_DIR)/../../../sPyNNaker/neural_modelling)))

# Work out the top-level project folder
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
EXTRA_MODELS_DIR := $(abspath $(dir $(MAKEFILE_PATH))/../../)/

# This is where the building will happen
BUILD_DIR := $(EXTRA_MODELS_DIR)c_models/build/$(APP)/

# This is where the output .aplx files will go
APP_OUTPUT_DIR := $(EXTRA_MODELS_DIR)python_models8/model_binaries/

# This is where the extra source files are located
EXTRA_SRC_DIR := $(EXTRA_MODELS_DIR)c_models/src

# This location will be used to hold source files after log conversion
# which saves instruction space on the SpiNNaker machine
EXTRA_MODIFIED_DIR := $(EXTRA_MODELS_DIR)c_models/modified_src/

# This simply maps the source directory to the modified source directory
SOURCE_DIRS += $(EXTRA_SRC_DIR):$(EXTRA_MODIFIED_DIR)

# Import the main neural build Makefile
include $(SPYNNAKER_INSTALL_DIR)/make/neuron_only_build.mk
