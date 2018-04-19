ifndef NEURAL_MODELLING_DIRS
    $(error NEURAL_MODELLING_DIRS is not set.  Please define NEURAL_MODELLING_DIRS (possibly by running "source setup" in the neural_modelling folder within the sPyNNaker source folder))
endif

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))

# Make sure that APP_OUTPUT_DIR points to where you want the aplx files to go
APP_OUTPUT_DIR := $(abspath $(dir $(MAKEFILE_PATH)))/../../../../python_models8/model_binaries/)/

# For multiple src dirs see note below.
# Make sure EXTRA_SRC_DIR points to the source dir where your unmodified files are found
EXTRA_SRC_DIR := $(abspath $(dir $(MAKEFILE_PATH))/../src)

# We need another directory where the converted c code will go. 
EXTRA_MODIFIED_DIR := $(abspath $(dir $(MAKEFILE_PATH))/../modified_src)

# We need to 
EXTRA_LOG_DICT_FILE := $(EXTRA_MODIFIED_DIR)log_dict.dict
	
# Add the log_file to the list insures that modification is done before any build
LOG_DICT_FILES += $(LOG_DICT_FILE)

# We need to tell the compliler to use the modified code
CFLAGS += -I$(EXTRA_MODIFIED_DIR)

# Make sure each neuron has a unique build dir
BUILD_DIR := $(abspath $(dir $(MAKEFILE_PATH)))/../builds/$(APP)/

# Support Function for converting src paths to modified paths
# $(NEURAL_MODELLING_DIRS)/src is done by neural_build.mk so not needed here
# This function if defined is called from within convert_to_modified
define extra_convert_to_modified
$(patsubst $(EXTRA_SRC_DIR)%,$(EXTRA_MODIFIED_DIR)%,$(1))
endef

# Support Function for converting modified c paths to object paths
# $(NEURAL_MODELLING_DIRS)..... is done by neural_build.mk so not needed here
# This function if defined is called from within convert_to_object
define extra_convert_to_object
$(patsubst $(EXTRA_MODIFIED_DIR)%.c, $(BUILD_DIR)%.o, $(1))
endef

include $(NEURAL_MODELLING_DIRS)/makefiles/neuron/neural_build.mk

# TODO
LFLAGS += $(MODIFIED_DIR)


# EXTRA_SYNAPSE_TYPE_OBJECTS is depricated!
# Instead add a new rule
#$(BUILD_DIR).....o: $(EXTRA_MODIFIED_DIR)...c $(C_FILES_MODIFIED)
#	-mkdir -p $(dir $@)
#	$(SYNAPSE_TYPE_COMPILE) -o $@ $<

                       
# EXTRA_STDP is depricated
# Instead add a new rule
#$(BUILD_DIR).....o: $(EXTRA_MODIFIED_DIR)...c $(C_FILES_MODIFIED)
#	-mkdir -p $(dir $@)
#	$(STDP_COMPILE) -o $@ $<

#Extra rules to copy the extra code
$(EXTRA_MODIFIED_DIR)%.c: $(EXTRA_SRC_DIR)%.c
	python -m spinn_utilities.make_tools.convertor $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE) 

$(EXTRA_MODIFIED_DIR)%.h: $(EXTRA_SRC_DIR)%.h
	python -m spinn_utilities.make_tools.convertor $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE) 

$(EXTRA_LOG_DICT_FILE): $(EXTRA_SRC_DIR)
	python -m spinn_utilities.make_tools.convertor $(EXTRA_SRC_DIR) $(EXTRA_MODIFIED_DIR) $(EXTRA_LOG_DICT_FILE) 

# build rule for the extra stuff
$(BUILD_DIR)%.o: $(EXTRA_MODIFIED_DIR)%.c $(C_FILES_MODIFIED)
	# extra build
	-mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<

test:
	# $(NEURON_MODEL) 
	# $(NEURON_MODEL_O)
	# $(call extra_convert_to_object, $(NEURON_MODEL_O))
	# $(EXTRA_MODIFIED_DIR)

# NOTE:
# $(NEURAL_MODELLING_DIRS)/makefiles/neuron/neural_build.mk brings in all code for $(NEURAL_MODELLING_DIRS).....

# If more that one extra src dir (not children) is required here you need to do the following for each source
# 1. Define a directory to place the modified code into (like EXTRA_MODIFIED_DIR)
# 2. Define a file to store the dictionary mappings into (like EXTRA_LOG_DICT_FILE)
# 3. Add each modified directory to the CFLAGS
# 4. Add each dictionary file to LOG_DICT_FILES
# 5. Extend extra_convert_to_modified so it converts all the src dirs to modified dirs
# 6. Extend extra_convert_to_object so it converts all the modified dirs to build dir
# 7. Add Extra rules to copy the extra code for each dir (both rules)
# 8. Add build rule for the extra stuff for each dir

