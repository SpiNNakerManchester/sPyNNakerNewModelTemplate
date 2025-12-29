MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(abspath $(dir $(MAKEFILE_PATH)))
APP_OUTPUT_DIR := $(CURRENT_DIR)/../python_models8/model_binaries/

DIRS = makefiles

all: $(DIRS)
	for d in $(DIRS); do $(MAKE) -C $$d || exit $$?; done

clean: $(DIRS)
	$(RM) $(APP_OUTPUT_DIR)logs.sqlite3
	$(RM) $(APP_OUTPUT_DIR)*.aplx
	$(RM) -r $(CURRENT_DIR)/modified_src
	for d in $(DIRS); do $(MAKE) -C $$d clean || exit $$?; done
