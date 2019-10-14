# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import spynnaker8 as sim
from spynnaker8.utilities import neo_convertor
from .nwt_testbase import NwtTestBase
from python_models8.neuron.builds.recording_neuron import RecordingNeuron

# Set the run time of the execution
run_time = 1000


class TestRecordingNeuron(NwtTestBase):

    def check_results(self, neo, expected_spikes):
        spikes = neo_convertor.convert_spikes(neo)
        v = neo_convertor.convert_data(neo, name="v")
        v_float = neo_convertor.convert_data(neo, name="v_float")
        v_double = neo_convertor.convert_data(neo, name="v_double")
        print(spikes)
        for i, spike in enumerate(expected_spikes):
            self.assertEqual(spikes[i][1], spike)
        self.assertEqual(spikes.shape, (len(spikes), 2))
        for spike in expected_spikes:
            self.assertTrue(v[spike][2] > v[spike+1][2])
        for i in range(len(v)):
            self.assertAlmostEqual(
                v[i][2] * 1.000001, v_double[i][2], delta=0.000001)

        self.assertEqual(len(v), len(v_float) * 4)
        v_index = 0
        f_index = 0
        found = 0
        while f_index < len(v_float):
            # Skip v while it is the wrong neuron
            while v[v_index][0] != v_float[f_index][0]:
                v_index += 1
            # Skip v while it is the wrong time
            while v[v_index][1] != v_float[f_index][1]:
                v_index += 1
            self.assertAlmostEqual(
                v[v_index][2] * 1.1, v_float[f_index][2], delta=0.000001)
            found += 1
            v_index += 1
            f_index += 1
        self.assertEqual(found, len(v_float))


    def do_run(self):
        sim.setup(timestep=1.0)
        input_pop = sim.Population(
            1, sim.SpikeSourceArray(range(0, run_time, 100)), label="input")
        test_pop = sim.Population(
            4, RecordingNeuron(), label="my_full_neuron")
        test_pop.record(['spikes', 'v', 'v_double'])
        # Even here we support selective recording
        test_pop.record(['v_float'], sampling_interval=2,
                             indexes=[1, 3])
        sim.Projection(
            input_pop, test_pop, sim.AllToAllConnector(),
            receptor_type='excitatory',
            synapse_type=sim.StaticSynapse(weight=2.0))
        sim.run(run_time)
        neo = test_pop.get_data('all')
        sim.end()
        self.check_results(neo, [501])

    def test_do_run(self):
        self.runsafe(self.do_run)
