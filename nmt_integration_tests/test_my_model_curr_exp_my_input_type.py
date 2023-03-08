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
from python_models8.neuron.builds.my_model_curr_exp_my_input_type import (
    MyModelCurrExpMyInputType)

# Set the run time of the execution
run_time = 1000


class TestMyModelCurrExpMyInputType(NwtTestBase):

    def do_run(self):
        sim.setup(timestep=1.0)
        input_pop = sim.Population(
            1, sim.SpikeSourceArray(range(0, run_time, 100)), label="input")
        test_pop = sim.Population(
            1, MyModelCurrExpMyInputType(
                my_input_parameter=1.0, my_multiplicator=1.0),
            label="my_model_my_input_type_pop")
        test_pop.record(['spikes', 'v'])
        sim.Projection(
            input_pop, test_pop, sim.AllToAllConnector(),
            receptor_type='excitatory',
            synapse_type=sim.StaticSynapse(weight=2.0))
        sim.run(run_time)
        neo = test_pop.get_data('all')
        sim.end()
        self.check_results(
            neo, [6, 10, 16, 102, 107, 112, 121, 204, 208, 213, 225, 305, 309,
                  314, 332, 406, 410, 416, 502, 507, 512, 521, 604, 608, 613,
                  625, 705, 709, 714, 732, 806, 810, 816, 902, 907, 912, 921])

    def test_do_run(self):
        self.runsafe(self.do_run)
