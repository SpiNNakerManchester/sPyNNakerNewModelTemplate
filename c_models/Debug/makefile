################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include src/neuron/plasticity/stdp/weight_dependence/subdir.mk
-include src/neuron/plasticity/stdp/timing_dependence/subdir.mk
-include src/neuron/models/subdir.mk
-include src/neuron/builds/my_model_curr_my_synapse_type/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_my_synapse_type/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_my_synapse_type/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp_stdp_mad_my_timing_my_weight/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp_stdp_mad_my_timing_my_weight/build/neuron/plasticity/stdp/subdir.mk
-include src/neuron/builds/my_model_curr_exp_stdp_mad_my_timing_my_weight/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_threshold/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_threshold/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_threshold/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_input_type/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_input_type/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_input_type/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_additional_input/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_additional_input/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_exp_my_additional_input/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp_incl_input_and_threshold/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp_incl_input_and_threshold/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_exp_incl_input_and_threshold/build/neuron/subdir.mk
-include src/neuron/builds/my_model_curr_exp/build/neuron/population_table/subdir.mk
-include src/neuron/builds/my_model_curr_exp/build/neuron/plasticity/subdir.mk
-include src/neuron/builds/my_model_curr_exp/build/neuron/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: sPyNNaker8NewModelTemplate_c_code

# Tool invocations
sPyNNaker8NewModelTemplate_c_code: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: Cross GCC Linker'
	arm-none-eabi-gcc  -o "sPyNNaker8NewModelTemplate_c_code" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(EXECUTABLES)$(OBJS)$(C_DEPS) sPyNNaker8NewModelTemplate_c_code
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
