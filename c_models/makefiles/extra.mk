ifndef NEURAL_MODELLING_DIRS
    $(error NEURAL_MODELLING_DIRS is not set.  Please define NEURAL_MODELLING_DIRS (possibly by running "source setup" in the neural_modelling folder within the sPyNNaker source folder))
endif

EXTRA_MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))

#Note: neural_build.mk will abspath and add any ending / as needed so DIRs can be in .. format here

# Make sure that APP_OUTPUT_DIR points to where you want the aplx files to go
APP_OUTPUT_DIR := $(dir $(EXTRA_MAKEFILE_PATH))../../python_models8/model_binaries/

# For multiple src dirs see note below.
# Make sure EXTRA_SRC_DIR points to the source dir where your unmodified files are found
EXTRA_SRC_DIR := $(abspath $(dir $(EXTRA_MAKEFILE_PATH))/../src)

# We need another directory where the converted c code will go. 
EXTRA_MODIFIED_DIR := $(abspath $(dir $(EXTRA_MAKEFILE_PATH))/../modified_src)

# We need to 
EXTRA_LOG_DICT_FILE := $(EXTRA_MODIFIED_DIR)/log_dict.dict
	
# Add the log_file to the list insures that modification is done before any build
# It also insures they are added to the final app dict file
LOG_DICT_FILES += $(LOG_DICT_FILE)

# We need to tell the compliler to use the modified code
CFLAGS += -I$(EXTRA_MODIFIED_DIR)

# Make sure each neuron has a unique build dir
BUILD_DIR := $(dir $(EXTRA_MAKEFILE_PATH)))/../build/$(APP)

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

# EXTRA_SYNAPSE_TYPE_OBJECTS is depricated!
# Instead add a new rule
#$(BUILD_DIR).....o: $(EXTRA_MODIFIED_DIR)...c $(C_FILES_MODIFIED)
#	-mkdir -p $(dir $@)
#	$(SYNAPSE_TYPE_COMPILE) -o $@ make$<

                       
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

# Add the extra modified dirs to the clean rule
EXTRA_CLEAN_DIRS += $(EXTRA_MODIFIED_DIR)

# Optional: Add these to the precious rule so they are not automatically removed by make
EXTRA_PRECIOUS += $(EXTRA_MODIFIED_DIR)%.c $(EXTRA_MODIFIED_DIR)%.h $(EXTRA_LOG_DICT_FILE)

# NOTE:
# $(NEURAL_MODELLING_DIRS)/makefiles/neuron/neural_build.mk brings in all code for $(NEURAL_MODELLING_DIRS).....

# If more that one extra src dir (not children) is required here you need to do the following for each source
# 1. Define a directory to place the modified code into (like EXTRA_MODIFIED_DIR)
# 2. Add each modified directory to the CFLAGS
# 3. Add each modified dir to EXTRA_CLEAN_DIRS so the are removed on clean
# 4. For each modified dir add a dir%.c and a dir%.h to EXTRA_PRECIOUS (optional)
# 5. Define a file to store the dictionary mappings into (like EXTRA_LOG_DICT_FILE)
# 6  Add each dictionary file to LOG_DICT_FILES
# 7. Add each dictionary file to EXTRA_PRECIOUS (optional)
# 8. Extend extra_convert_to_modified so it converts all the src dirs to modified dirs
# 9. Extend extra_convert_to_object so it converts all the modified dirs to build dir
# 10. Add Extra rules to copy the extra code for each dir (both rules)
# 11. Add build rule for the extra stuff for each dir
