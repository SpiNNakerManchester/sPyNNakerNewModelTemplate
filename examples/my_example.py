# import spynnaker8 and plotting stuff
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

# import models
from python_models8.model_data_holders.my_model_curr_exp_data_holder \
    import MyModelCurrExpDataHolder as My_Model_Curr_Exp
from python_models8.model_data_holders\
    .my_model_curr_exp_my_additional_input_data_holder \
    import MyModelCurrExpMyAdditionalInputDataHolder as \
    My_Model_Curr_Exp_My_Additional_Input
from python_models8.model_data_holders\
    .my_model_curr_exp_my_threshold_data_holder \
    import MyModelCurrExpMyThresholdDataHolder \
    as My_Model_Curr_Exp_My_Threshold
from python_models8.model_data_holders\
    .my_model_curr_my_synapse_type_data_holder \
    import MyModelCurrMySynapseTypeDataHolder as My_Model_Curr_My_Synapse_Type
from python_models8.neuron.plasticity.stdp.timing_dependence\
    .my_timing_dependence import MyTimingDependence
from python_models8.neuron.plasticity.stdp.weight_dependence\
    .my_weight_dependence import MyWeightDependence


# Set the run time of the execution
run_time = 1000

# Set the time step of the simulation in milliseconds
time_step = 1.0

# Set the number of neurons to simulate
n_neurons = 1

# Set the i_offset current
i_offset = 0.0

# Set the weight of input spikes
weight = 2.0

# Set the times at which to input a spike
spike_times = range(0, run_time, 100)

p.setup(time_step)

spikeArray = {"spike_times": spike_times}
input_pop = p.Population(
    1, p.SpikeSourceArray(**spikeArray), label="input")

myModelCurrExpParams = {
    "my_parameter": -70.0,
    "i_offset": i_offset
}
my_model_pop = p.Population(
    1, My_Model_Curr_Exp(**myModelCurrExpParams),
    label="my_model_pop")
p.Projection(
    input_pop, my_model_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

myModelCurrMySynapseTypeParams = {
    "my_parameter": -70.0,
    "i_offset": i_offset,
    "my_ex_synapse_parameter": 0.5
}
my_model_my_synapse_type_pop = p.Population(
    1, My_Model_Curr_My_Synapse_Type(**myModelCurrMySynapseTypeParams),
    label="my_model_my_synapse_type_pop")
p.Projection(
    input_pop, my_model_my_synapse_type_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

myModelCurrExpMyAdditionalInputParams = {
    "my_parameter": -70.0,
    "i_offset": i_offset,
    "my_additional_input_parameter": 0.05
}
my_model_my_additional_input_pop = p.Population(
    1, My_Model_Curr_Exp_My_Additional_Input(
        **myModelCurrExpMyAdditionalInputParams),
    label="my_model_my_additional_input_pop")
p.Projection(
    input_pop, my_model_my_additional_input_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

myModelCurrExpMyThresholdParams = {
    "my_parameter": -70.0,
    "i_offset": i_offset,
    "threshold_value": -10.0,
    "my_threshold_parameter": 0.4
}
my_model_my_threshold_pop = p.Population(
    1, My_Model_Curr_Exp_My_Threshold(**myModelCurrExpMyThresholdParams),
    label="my_model_my_threshold_pop")
p.Projection(
    input_pop, my_model_my_threshold_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_stdp_pop = p.Population(
    1, My_Model_Curr_Exp(**myModelCurrExpParams),
    label="my_model_pop")
stdp = p.STDPMechanism(
    timing_dependence=MyTimingDependence(
        my_potentiation_parameter=2.0,
        my_depression_parameter=0.1),
    weight_dependence=MyWeightDependence(
        w_min=0.0, w_max=10.0, my_parameter=0.5))
p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))
stdp_connection = p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(),
    synapse_type=stdp)

my_model_pop.record(['v'])
my_model_my_synapse_type_pop.record(['v'])
my_model_my_additional_input_pop.record(['v'])
my_model_my_threshold_pop.record(['v'])

# my_model_pop.set(my_neuron_parameter=-60.0)
# my_model_my_synapse_type_pop.set(my_ex_synapse_parameter=1.5)
# my_model_my_additional_input_pop.set(my_additional_input_parameter=0.01)
# my_model_my_threshold_pop.set(my_threshold_parameter=1.0)

p.run(run_time)

print stdp_connection.get('weight', 'list')

# get v for each example
v_my_model_pop = my_model_pop.get_data('v')
v_my_model_my_synapse_type_pop = my_model_my_synapse_type_pop.get_data('v')
v_my_model_my_additional_input_pop = my_model_my_additional_input_pop.get_data(
    'v')
v_my_model_my_threshold_pop = my_model_my_threshold_pop.get_data('v')

Figure(
    # membrane potentials for each example
    Panel(v_my_model_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_pop.label], yticks=True, xlim=(0, run_time)),
    Panel(v_my_model_my_synapse_type_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_my_synapse_type_pop.label],
          yticks=True, xlim=(0, run_time)),
    Panel(v_my_model_my_additional_input_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_my_additional_input_pop.label],
          yticks=True, xlim=(0, run_time)),
    Panel(v_my_model_my_threshold_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_my_threshold_pop.label],
          yticks=True, xlim=(0, run_time)),
    title="Simple my model examples",
    annotations="Simulated with {}".format(p.name())
)
plt.show()

p.end()
