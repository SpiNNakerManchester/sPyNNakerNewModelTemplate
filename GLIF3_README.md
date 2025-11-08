# GLIF3 Neuron Model Implementation

This repository now includes an implementation of the GLIF3 (Generalized Leaky Integrate-and-Fire) neuron model for sPyNNaker.

## Overview

The GLIF3 model is a biologically-inspired point neuron model developed by the Allen Institute for Brain Science. It extends the classic leaky integrate-and-fire model with **after-spike currents** that capture spike frequency adaptation and other longer-term effects.

### Key Features

- **Leaky integrate-and-fire dynamics**: Standard LIF membrane voltage equation
- **Two after-spike currents**: Fast and slow components with independent time constants
- **Fixed threshold**: Constant spike threshold
- **Refractory period**: Post-spike refractory behavior
- **Exponential synapses**: Standard exponential current-based synapses

## Model Equations

### Membrane Voltage Dynamics

Between spikes, the membrane voltage V(t) evolves according to:

```
dV/dt = (1/C_m) * [I_e(t) + I_asc_0(t) + I_asc_1(t) - g*(V(t) - E_L)]
```

Where:
- `C_m` = membrane capacitance (nF)
- `I_e(t)` = external/synaptic input current (nA)
- `I_asc_0(t)`, `I_asc_1(t)` = fast and slow after-spike currents (nA)
- `g` = membrane conductance (µS)
- `E_L` = resting potential (mV)

### After-Spike Current Dynamics

The after-spike currents decay exponentially:

```
dI_asc_j/dt = -k_j * I_asc_j(t),  for j = 0, 1
```

Where:
- `k_j = 1/τ_j` is the decay rate (1/ms)
- `τ_j` is the time constant (ms)

### Spike and Reset

When `V(t) >= V_thresh`, the neuron spikes and:

1. Voltage resets: `V → V_reset`
2. After-spike currents update: `I_asc_j → I_asc_j * exp(-k_j * t_ref) + asc_amp_j`
3. Refractory period `t_ref` begins (neuron cannot spike)

## Parameters

| Parameter | Symbol | Default | Units | Description |
|-----------|--------|---------|-------|-------------|
| `c_m` | C_m | 1.0 | nF | Membrane capacitance |
| `e_l` | E_L | -70.0 | mV | Resting potential |
| `v_reset` | V_reset | -70.0 | mV | Reset voltage |
| `v_thresh` | V_thresh | -50.0 | mV | Spike threshold |
| `asc_amp_0` | δI_0 | 0.0 | nA | Fast after-spike current amplitude |
| `asc_amp_1` | δI_1 | 0.0 | nA | Slow after-spike current amplitude |
| `g` | g | 0.05 | µS | Membrane conductance |
| `k0` | k_0 | 0.2 | 1/ms | Fast ASC decay rate (τ_0 = 5 ms) |
| `k1` | k_1 | 0.05 | 1/ms | Slow ASC decay rate (τ_1 = 20 ms) |
| `t_ref` | t_ref | 2.0 | ms | Refractory period |
| `i_offset` | I_offset | 0.0 | nA | Constant input current |
| `tau_syn_E` | τ_syn_E | 5.0 | ms | Excitatory synapse time constant |
| `tau_syn_I` | τ_syn_I | 5.0 | ms | Inhibitory synapse time constant |

## Files Added/Modified

### Python Implementation
- `python_models8/neuron/neuron_models/glif3_neuron_model.py` - Core GLIF3 neuron model
- `python_models8/neuron/builds/glif3_curr.py` - PyNN model interface with current-based synapses

### C Implementation
- `c_models/src/my_models/models/glif3_neuron_impl.h` - C neuron model implementation

### Build Configuration
- `c_models/makefiles/glif3_curr/Makefile` - Build configuration for GLIF3 model
- `c_models/makefiles/Makefile` - Updated to include GLIF3 model

### Examples
- `examples/glif3_example.py` - Example usage script

## Usage Example

```python
import pyNN.spiNNaker as sim
from python_models8.neuron.builds.glif3_curr import GLIF3Curr

# Setup simulation
sim.setup(timestep=1.0)

# Create GLIF3 neurons with after-spike currents
cell_params = {
    'c_m': 1.0,
    'e_l': -70.0,
    'v_reset': -70.0,
    'v_thresh': -50.0,
    'asc_amp_0': -5.0,  # Hyperpolarizing fast ASC
    'asc_amp_1': -2.0,  # Hyperpolarizing slow ASC
    'g': 0.05,
    'k0': 0.5,          # Fast decay (τ = 2 ms)
    'k1': 0.05,         # Slow decay (τ = 20 ms)
    't_ref': 2.0,
    'i_offset': 1.0,
}

pop = sim.Population(10, GLIF3Curr(**cell_params), label="GLIF3_neurons")

# Record and run
pop.record(['spikes', 'v'])
sim.run(1000.0)

# Retrieve data
spikes = pop.get_data('spikes')
voltage = pop.get_data('v')

sim.end()
```

## Building

To build the GLIF3 model for SpiNNaker:

1. Ensure you have sPyNNaker installed and configured
2. Source the sPyNNaker setup script to set environment variables
3. Build the model:

```bash
cd c_models
make
```

This will compile the GLIF3 binary (`glif3_curr.aplx`) along with other models.

## References

1. **Teeter C, Iyer R, Menon V, et al.** (2018). "Generalized leaky integrate-and-fire models classify multiple neuron types." *Nature Communications* 9:709. DOI: [10.1038/s41467-017-02717-4](https://doi.org/10.1038/s41467-017-02717-4)

2. **Allen Institute for Brain Science** (2023). Allen Cell Types Database. Available from: [http://celltypes.brain-map.org/](http://celltypes.brain-map.org/)

3. **Mihalas S, Niebur E** (2009). "A generalized linear integrate-and-fire neural model produces diverse spiking behaviors." *Neural Computation* 21(3):704-718.

## Model Hierarchy

The GLIF model family includes 5 levels of increasing complexity:

- **GLIF1**: Basic LIF with fixed threshold
- **GLIF2**: GLIF1 + reset rules and spike-induced threshold adaptation
- **GLIF3**: GLIF1 + after-spike currents (this implementation)
- **GLIF4**: GLIF2 + GLIF3 (reset rules + after-spike currents)
- **GLIF5**: GLIF4 + voltage-dependent threshold adaptation

This implementation focuses on GLIF3, which provides spike frequency adaptation through after-spike currents while maintaining computational efficiency.

## Testing

Run the example script to test the implementation:

```bash
python examples/glif3_example.py
```

## Parameter Tuning

### Spike Frequency Adaptation

To create spike frequency adaptation (neurons fire less frequently over time):
- Set `asc_amp_0` and `asc_amp_1` to negative values (hyperpolarizing)
- Adjust `k0` and `k1` to control adaptation time scales
- Typical values: `asc_amp_0 = -5.0 nA`, `asc_amp_1 = -2.0 nA`

### Regular Spiking

For regular spiking without adaptation:
- Set `asc_amp_0 = 0.0` and `asc_amp_1 = 0.0`
- This reduces GLIF3 to a basic LIF model

### Fast vs Slow Adaptation

- Fast adaptation: Use larger `k0` (smaller τ_0)
- Slow adaptation: Use smaller `k1` (larger τ_1)
- Typical time constants: τ_0 = 2-10 ms, τ_1 = 20-100 ms

## License

This implementation follows the sPyNNaker template license. The GLIF model equations and concepts are based on work by the Allen Institute for Brain Science (BSD-style license with non-commercial clause).
