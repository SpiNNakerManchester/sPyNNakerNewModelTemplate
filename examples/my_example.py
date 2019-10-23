# import spynnaker8 and plotting stuff
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

# import models
from python_models8.neuron.plasticity.stdp.timing_dependence\
    .my_timing_dependence import (
        MyTimingDependence)
from python_models8.neuron.plasticity.stdp.weight_dependence\
    .my_weight_dependence import (
        MyWeightDependence)
from python_models8.neuron.builds.my_model_curr_exp import MyModelCurrExp
from python_models8.neuron.builds.my_full_neuron import MyFullNeuron
from python_models8.neuron.builds.my_if_curr_exp_sEMD import MyIFCurrExpSEMD
from python_models8.neuron.builds.my_model_curr_exp_my_input_type import (
    MyModelCurrExpMyInputType)
from python_models8.neuron.builds.my_model_curr_my_synapse_type import (
    MyModelCurrMySynapseType)
from python_models8.neuron.builds.my_model_curr_exp_my_additional_input \
    import (
        MyModelCurrExpMyAdditionalInput)
from python_models8.neuron.builds.my_model_curr_exp_my_threshold import (
    MyModelCurrExpMyThreshold)


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
    n_neurons, p.SpikeSourceArray(**spikeArray), label="input")

my_model_pop = p.Population(
    1, MyModelCurrExp(my_neuron_parameter=-70.0, i_offset=i_offset),
    label="my_model_pop")
p.Projection(
    input_pop, my_model_pop, p.AllToAllConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

myModelCurrExpMyInputTypeParams = {
    "my_input_parameter": 1.0,
    "my_multiplicator": 1.0
}
my_model_my_input_type_pop = p.Population(
    n_neurons, MyModelCurrExpMyInputType(
        my_input_parameter=1.0, my_multiplicator=1.0),
    label="my_model_my_input_type_pop")
p.Projection(
    input_pop, my_model_my_input_type_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_my_synapse_type_pop = p.Population(
    n_neurons, MyModelCurrMySynapseType(
        my_neuron_parameter=-70.0, i_offset=i_offset,
        my_ex_synapse_parameter=0.5),
    label="my_model_my_synapse_type_pop")
p.Projection(
    input_pop, my_model_my_synapse_type_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_my_additional_input_pop = p.Population(
    n_neurons, MyModelCurrExpMyAdditionalInput(
        my_neuron_parameter=-70.0, i_offset=i_offset,
        my_additional_input_parameter=0.05),
    label="my_model_my_additional_input_pop")
p.Projection(
    input_pop, my_model_my_additional_input_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_my_threshold_pop = p.Population(
    n_neurons, MyModelCurrExpMyThreshold(
        my_neuron_parameter=-70.0, i_offset=i_offset, threshold_value=-10.0,
        my_threshold_parameter=0.4),
    label="my_model_my_threshold_pop")
p.Projection(
    input_pop, my_model_my_threshold_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_stdp_pop = p.Population(
    n_neurons, MyModelCurrExp(i_offset=i_offset), label="my_model_pop")
stdp = p.STDPMechanism(
    timing_dependence=MyTimingDependence(
        my_potentiation_parameter=2.0,
        my_depression_parameter=0.1),
    weight_dependence=MyWeightDependence(
        w_min=0.0, w_max=10.0, my_weight_parameter=0.5))
p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))
stdp_connection = p.Projection(
    input_pop, my_model_stdp_pop,
    p.OneToOneConnector(),
    synapse_type=stdp)

my_if_curr_exp_semd_pop = p.Population(
    n_neurons, MyIFCurrExpSEMD(
        my_multiplicator=0.0, my_inh_input_previous=0.0),
    label="my_if_curr_exp_semd_pop")
p.Projection(
    input_pop, my_if_curr_exp_semd_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=5.0))

my_full_neuron_pop = p.Population(
    n_neurons, MyFullNeuron(), label="my_full_neuron_pop")
p.Projection(
    input_pop, my_full_neuron_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))

my_model_pop.record(['v'])
my_model_my_input_type_pop.record(['v'])
my_model_my_synapse_type_pop.record(['v'])
my_model_my_additional_input_pop.record(['v'])
my_model_my_threshold_pop.record(['v'])
my_if_curr_exp_semd_pop.record(['v'])
my_full_neuron_pop.record(['v'])

p.run(run_time)

print(stdp_connection.get('weight', 'list'))

# get v for each example
v_my_model_pop = my_model_pop.get_data('v')
v_my_model_my_input_type_pop = my_model_my_input_type_pop.get_data('v')
v_my_model_my_synapse_type_pop = my_model_my_synapse_type_pop.get_data('v')
v_my_model_my_additional_input_pop = my_model_my_additional_input_pop.get_data(
    'v')
v_my_model_my_threshold_pop = my_model_my_threshold_pop.get_data('v')
v_my_if_curr_exp_semd_pop = my_if_curr_exp_semd_pop.get_data('v')
v_my_full_neuron_pop = my_full_neuron_pop.get_data('v')

Figure(
    # membrane potentials for each example
    Panel(v_my_model_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_pop.label], yticks=True, xlim=(0, run_time)),
    Panel(v_my_model_my_input_type_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_model_my_input_type_pop.label],
          yticks=True, xlim=(0, run_time)),
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
    Panel(v_my_if_curr_exp_semd_pop.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[my_if_curr_exp_semd_pop.label],
          yticks=True, xlim=(0, run_time)),
    Panel(v_my_full_neuron_pop.segments[0].filter(name='v')[0],
          xlabel="Time (ms)",
          ylabel="Membrane potential (mV)",
          data_labels=[my_full_neuron_pop.label],
          yticks=True, xlim=(0, run_time), xticks=True),
    title="Simple my model examples",
    annotations="Simulated with {}".format(p.name())
)
plt.show()

p.end()
