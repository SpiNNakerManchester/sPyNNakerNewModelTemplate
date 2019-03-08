# import spynnaker8 and plotting stuff
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

# import models
from python_models8.neuron.builds.my_full_neuron import MyFullNeuron
from python_models8.neuron.builds.drl_lif_neuron import DRLLIFNeuron

# Set the run time of the execution
run_time = 5000

# Set the time step of the simulation in milliseconds
time_step = 1.0  # 0.1

# Set the number of neurons to simulate
n_neurons = 2

# Set the i_offset current
i_offset = 0.0

# Set the weight of input spikes
weight = 3.0

# Set the times at which to input a spike
spike_times1 = range(0, run_time, 1000)
spike_times2 = range(100, run_time, 1000)

print('spike_times are ', spike_times1, spike_times2)

p.setup(time_step)

all_spikes = []
for n in range(n_neurons//2):
    all_spikes.append(spike_times1)
    all_spikes.append(spike_times2)

spikeArray = {"spike_times": all_spikes} # [spike_times1, spike_times2]}
input_pop = p.Population(
    n_neurons, p.SpikeSourceArray(**spikeArray), label="input")

my_full_neuron_pop = p.Population(
    n_neurons, MyFullNeuron(), label="my_full_neuron")
p.Projection(
    input_pop, my_full_neuron_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight, delay=1))

drl_lif_neuron_pop = p.Population(
    n_neurons, DRLLIFNeuron(), label="drl_lif_neuron")
p.Projection(
    input_pop, drl_lif_neuron_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight, delay=1))

standard_ifcurr_pop = p.Population(
    n_neurons, p.IF_curr_exp(), label="standard_if_curr")
p.Projection(
    input_pop, standard_ifcurr_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight, delay=1))

standard_ifcurr_pop.set(v_thresh=-55.0)
#standard_ifcurr_pop.set(tau_syn_E=5.0)
standard_ifcurr_pop.set(tau_m=20.0)
#standard_ifcurr_pop.set(cm=5.0)
#standard_ifcurr_pop.set(tau_refrac=20.0)


my_full_neuron_pop.record(['v', 'spikes'])
drl_lif_neuron_pop.record(['v', 'spikes'])
standard_ifcurr_pop.record(['v', 'spikes'])

p.run(run_time)

# get v for each example
v_my_full_neuron_pop = my_full_neuron_pop.get_data('v')
v_drl_lif_neuron_pop = drl_lif_neuron_pop.get_data('v')
v_standard_ifcurr_pop = standard_ifcurr_pop.get_data('v')
spikes_my_full_neuron_pop = my_full_neuron_pop.get_data('spikes')
spikes_drl_lif_neuron_pop = drl_lif_neuron_pop.get_data('spikes')
spikes_standard_ifcurr_pop = standard_ifcurr_pop.get_data('spikes')

spikes_full = my_full_neuron_pop.spinnaker_get_data('spikes')
print(spikes_full)
spikes_drl = drl_lif_neuron_pop.spinnaker_get_data('spikes')
print(spikes_drl)
spikes_standard = standard_ifcurr_pop.spinnaker_get_data('spikes')
print(spikes_standard)

Figure(
    # membrane potentials for each example: standard
    Panel(spikes_standard_ifcurr_pop.segments[0].spiketrains,
          ylabel="IFCurr Neuron ID",
          yticks=True, markersize=1.5, xlim=(0, run_time)),
    Panel(v_standard_ifcurr_pop.segments[0].filter(name='v')[0],
          xlabel="Time (ms)",
          ylabel="Membrane potential (mV)",
          data_labels=[standard_ifcurr_pop.label],
          yticks=True, xlim=(0, run_time), xticks=True),
    # DRL
    Panel(spikes_drl_lif_neuron_pop.segments[0].spiketrains,
          ylabel="DRL Neuron ID",
          yticks=True, markersize=1.5, xlim=(0, run_time)),
    Panel(v_drl_lif_neuron_pop.segments[0].filter(name='v')[0],
          xlabel="Time (ms)",
          ylabel="Membrane potential (mV)",
          data_labels=[drl_lif_neuron_pop.label],
          yticks=True, xlim=(0, run_time), xticks=True),
    # our toy full neuron example
    Panel(spikes_my_full_neuron_pop.segments[0].spiketrains,
          ylabel="Neuron ID",
          yticks=True, markersize=1.5, xlim=(0, run_time)),
    Panel(v_my_full_neuron_pop.segments[0].filter(name='v')[0],
          xlabel="Time (ms)",
          ylabel="Membrane potential (mV)",
          data_labels=[my_full_neuron_pop.label],
          yticks=True, xlim=(0, run_time), xticks=True),
    title="Simple my model examples (IFCurr, DRL)", # ", full)",
    annotations="Simulated with {}".format(p.name())
)
plt.show()

p.end()
