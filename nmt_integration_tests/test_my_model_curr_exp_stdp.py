# Copyright (c) 2017 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyNN.spiNNaker as sim
from .nwt_testbase import NwtTestBase
from python_models8.neuron.builds.my_model_curr_exp import MyModelCurrExp
from python_models8.neuron.plasticity.stdp.timing_dependence\
    .my_timing_dependence import (
        MyTimingDependence)
from python_models8.neuron.plasticity.stdp.weight_dependence\
    .my_weight_dependence import (
        MyWeightDependence)

# Set the run time of the execution
run_time = 1000


class TestMyModelCurrExpSTDP(NwtTestBase):

    def do_run(self):
        sim.setup(timestep=1.0)
        input_pop = sim.Population(
            1, sim.SpikeSourceArray(range(0, run_time, 100)), label="input")
        test_pop = sim.Population(
            1, MyModelCurrExp(my_neuron_parameter=-70.0, i_offset=0.0),
            label="my_model_pop")
        test_pop.record(['spikes', 'v'])
        stdp = sim.STDPMechanism(
            timing_dependence=MyTimingDependence(
                my_potentiation_parameter=2.0,
                my_depression_parameter=0.1),
            weight_dependence=MyWeightDependence(
                w_min=0.0, w_max=10.0, my_weight_parameter=0.5))
        sim.Projection(
            input_pop, test_pop,
            sim.OneToOneConnector(), receptor_type='excitatory',
            synapse_type=sim.StaticSynapse(weight=2.0))
        stdp_connection = sim.Projection(
            input_pop, test_pop, sim.OneToOneConnector(),
            synapse_type=stdp)
        sim.run(run_time)
        weights = stdp_connection.get('weight', 'list')
        neo = test_pop.get_data('all')
        sim.end()
        for _, _, weight in weights:
            self.assertEqual(weight, 0.5)
        self.check_results(neo, [201, 402, 603, 804])

    def test_do_run(self):
        self.runsafe(self.do_run)
