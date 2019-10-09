# import spynnaker8 and plotting stuff
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

# import models
from python_models8.neuron.builds.recording_neuron import RecordingNeuron


# Set the run time of the execution
run_time = 20

# Set the time step of the simulation in milliseconds
time_step = 1.0

# Set the number of neurons to simulate
n_neurons = 1

# Set the i_offset current
i_offset = 0.0

# Set the weight of input spikes
weight = 2.0

# Set the times at which to input a spike
spike_times = range(0, run_time, 2)

p.setup(time_step)

spikeArray = {"spike_times": spike_times}
input_pop = p.Population(
    n_neurons, p.SpikeSourceArray(**spikeArray), label="input")

recording_pop = p.Population(
    n_neurons, RecordingNeuron(), label="recording_neuron_pop")
p.Projection(
    input_pop, recording_pop,
    p.OneToOneConnector(), receptor_type='excitatory',
    synapse_type=p.StaticSynapse(weight=weight))


recording_pop.record(['v', 'v_float'])

p.run(run_time)

# get v for each example
recording_pop_neo = recording_pop.get_data(['v','v_float'])
print(recording_pop_neo.segments[0].filter(name='v')[0])
print(recording_pop_neo.segments[0].filter(name='v_float')[0])

p.end()
