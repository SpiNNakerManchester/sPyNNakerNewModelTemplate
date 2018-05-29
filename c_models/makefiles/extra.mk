ifndef NEURAL_MODELLING_DIRS
    $(error NEURAL_MODELLING_DIRS is not set.  Please define NEURAL_MODELLING_DIRS (possibly by running "source setup" in the neural_modelling folder within the sPyNNaker source folder))
endif

# ----------------------------------------------------------------------
# Compute the absolute path to the directory containing this file.
#
EXTRA_MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))

# Note: neural_build.mk will use abspath and add a final slash character as
# needed, so DIRs can be in .. format here

# ----------------------------------------------------------------------
# Make sure that APP_OUTPUT_DIR points to where you want the .aplx files to go.
#
APP_OUTPUT_DIR := $(dir $(EXTRA_MAKEFILE_PATH))../../python_models8/model_binaries/

# ----------------------------------------------------------------------
# For multiple source directories, see note below.
# Make sure EXTRA_SRC_DIR points to the source directory where your unmodified
# files are found.
#
EXTRA_SRC_DIR := $(abspath $(dir $(EXTRA_MAKEFILE_PATH))/../src)

# ----------------------------------------------------------------------
# We need another directory where the converted C code will go.
#
EXTRA_MODIFIED_DIR := $(abspath $(dir $(EXTRA_MAKEFILE_PATH))/../modified_src)

# ----------------------------------------------------------------------
# We need to point where the logging dictionary mappings will be stored.
#
EXTRA_LOG_DICT_FILE := $(EXTRA_MODIFIED_DIR)/log_dict.dict

# ----------------------------------------------------------------------
# Add the log_file to the list to ensure that they are brought up to date at
# the right stage of any build. It also ensures that they are added to the
# final app dictionary file.
#
LOG_DICT_FILES += $(LOG_DICT_FILE)

# ----------------------------------------------------------------------
# We need to tell the compliler to use the modified code.
#
CFLAGS += -I$(EXTRA_MODIFIED_DIR)

# ----------------------------------------------------------------------
# Make sure each neuron model has a unique build directory.
#
BUILD_DIR := $(dir $(EXTRA_MAKEFILE_PATH)))/../build/$(APP)

# ----------------------------------------------------------------------
# Support function for converting original source paths to modified paths.
#
# $(NEURAL_MODELLING_DIRS)/src is done by neural_build.mk so not needed here.
# This function, if defined, is called from within convert_to_modified.
#
define extra_convert_to_modified
$(patsubst $(EXTRA_SRC_DIR)%,$(EXTRA_MODIFIED_DIR)%,$(1))
endef

# ----------------------------------------------------------------------
# Support function for converting modified C paths to object paths.
#
# $(NEURAL_MODELLING_DIRS)..... is done by neural_build.mk so not needed here.
# This function, if defined, is called from within convert_to_object.
#
define extra_convert_to_object
$(patsubst $(EXTRA_MODIFIED_DIR)%.c, $(BUILD_DIR)%.o, $(1))
endef

# ----------------------------------------------------------------------

include $(NEURAL_MODELLING_DIRS)/makefiles/neuron/neural_build.mk

# ----------------------------------------------------------------------

# EXTRA_SYNAPSE_TYPE_OBJECTS is deprecated!
# Instead add a new rule
#$(BUILD_DIR).....o: $(EXTRA_MODIFIED_DIR)...c $(C_FILES_MODIFIED)
#	-mkdir -p $(dir $@)
#	$(SYNAPSE_TYPE_COMPILE) -o $@ make$<

                       
# EXTRA_STDP is deprecated
# Instead add a new rule
#$(BUILD_DIR).....o: $(EXTRA_MODIFIED_DIR)...c $(C_FILES_MODIFIED)
#	-mkdir -p $(dir $@)
#	$(STDP_COMPILE) -o $@ $<

# ----------------------------------------------------------------------
# Make rules to copy and transform the extra code (so that logging messages are
# compressed on SpiNNaker).
#
$(EXTRA_MODIFIED_DIR)%.c: $(EXTRA_SRC_DIR)%.c
	python -m spinn_utilities.make_tools.converter $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE)

$(EXTRA_MODIFIED_DIR)%.h: $(EXTRA_SRC_DIR)%.h
	python -m spinn_utilities.make_tools.converter $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE)

$(EXTRA_LOG_DICT_FILE): $(EXTRA_SRC_DIR)
	python -m spinn_utilities.make_tools.converter $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE)

# ----------------------------------------------------------------------
# Build rule for the transformed extra source files.
#
$(BUILD_DIR)%.o: $(EXTRA_MODIFIED_DIR)%.c $(C_FILES_MODIFIED)
	# extra build
	-mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<

# ----------------------------------------------------------------------
# Add the directories containing the extra transformed sources to the clean
# rule.
#
EXTRA_CLEAN_DIRS += $(EXTRA_MODIFIED_DIR)

# ----------------------------------------------------------------------
# Optional: Add these to the precious rule so they are not automatically
# removed by make.
#
EXTRA_PRECIOUS += $(EXTRA_MODIFIED_DIR)%.c $(EXTRA_MODIFIED_DIR)%.h $(EXTRA_LOG_DICT_FILE)

# NOTE:
# $(NEURAL_MODELLING_DIRS)/makefiles/neuron/neural_build.mk brings in all code
# for $(NEURAL_MODELLING_DIRS).....

# ----------------------------------------------------------------------
# If more that one extra source directory (not children) is required here, you
# need to do the following for each source.
#
#  1. Define a directory to place the modified code into (like
#     EXTRA_MODIFIED_DIR).
#  2. Add each modified directory to the CFLAGS.
#  3. Add each modified directory to EXTRA_CLEAN_DIRS so the are removed on
#     clean.
#  4. For each modified directory, add a dir%.c and a dir%.h to EXTRA_PRECIOUS
#     (optional).
#  5. Define a file to store the dictionary mappings into (like
#     EXTRA_LOG_DICT_FILE).
#  6  Add each dictionary file to LOG_DICT_FILES.
#  7. Add each dictionary file to EXTRA_PRECIOUS (optional).
#  8. Extend extra_convert_to_modified so it converts all the source
#     directories to modified directories.
#  9. Extend extra_convert_to_object so it converts all the modified
#     directories to build directory.
# 10. Add extra rules to copy the extra code for each directory (both rules).
# 11. Add build rule for the extra stuff for each directory.
