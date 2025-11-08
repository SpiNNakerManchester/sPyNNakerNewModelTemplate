"""
Example usage of the GLIF3 (Generalized Leaky Integrate-and-Fire) neuron model.

This example demonstrates how to create and simulate a GLIF3 neuron with
after-spike currents.
"""

import pyNN.spiNNaker as sim
from python_models8.neuron.builds.glif3_curr import GLIF3Curr

# Simulation parameters
sim_time = 1000.0  # ms
timestep = 1.0     # ms

# Setup the simulation
sim.setup(timestep=timestep)

# GLIF3 neuron parameters (example values)
cell_params = {
    'c_m': 1.0,           # Membrane capacitance (nF)
    'e_l': -70.0,         # Resting potential (mV)
    'v_reset': -70.0,     # Reset voltage (mV)
    'v_thresh': -50.0,    # Threshold voltage (mV)
    'asc_amp_0': -5.0,    # Fast after-spike current amplitude (nA) - hyperpolarizing
    'asc_amp_1': -2.0,    # Slow after-spike current amplitude (nA) - hyperpolarizing
    'g': 0.05,            # Membrane conductance (uS)
    'k0': 0.5,            # Fast ASC decay rate (1/ms) - tau_0 = 2 ms
    'k1': 0.05,           # Slow ASC decay rate (1/ms) - tau_1 = 20 ms
    't_ref': 2.0,         # Refractory period (ms)
    'i_offset': 1.0,      # Constant input current (nA)
    'tau_syn_E': 5.0,     # Excitatory synapse time constant (ms)
    'tau_syn_I': 5.0,     # Inhibitory synapse time constant (ms)
}

# Create a population of GLIF3 neurons
n_neurons = 10
pop_glif3 = sim.Population(
    n_neurons,
    GLIF3Curr(**cell_params),
    label="GLIF3_population"
)

# Create a spike source to provide input
spike_times = [[i * 50 + 10] for i in range(10)]  # Spikes every 50ms for each neuron
input_pop = sim.Population(
    n_neurons,
    sim.SpikeSourceArray(spike_times=spike_times),
    label="Input_spikes"
)

# Connect input to GLIF3 population
sim.Projection(
    input_pop,
    pop_glif3,
    sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=5.0, delay=1.0),
    receptor_type='excitatory'
)

# Record spikes and membrane voltage
pop_glif3.record(['spikes', 'v'])

# Run the simulation
sim.run(sim_time)

# Retrieve recorded data
spikes = pop_glif3.get_data('spikes')
voltage = pop_glif3.get_data('v')

# Print spike data
print("\nGLIF3 Neuron Spikes:")
print(f"Number of spikes: {len(spikes.segments[0].spiketrains[0])}")
if len(spikes.segments[0].spiketrains) > 0:
    print(f"First neuron spike times: {spikes.segments[0].spiketrains[0]}")

# End simulation
sim.end()

print("\nSimulation completed successfully!")
print("\nGLIF3 model features:")
print("- Leaky integrate-and-fire dynamics")
print("- Two after-spike currents with different time constants")
print("- Fixed threshold")
print("- Refractory period")
