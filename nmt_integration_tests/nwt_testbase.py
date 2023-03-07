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

from spinnaker_testbase import BaseTestCase
from spynnaker.pyNN.utilities import neo_convertor


class NwtTestBase(BaseTestCase):

    def check_results(self, neo, expected_spikes):
        spikes = neo_convertor.convert_spikes(neo)
        v = neo_convertor.convert_data(neo, name="v")
        print(spikes)
        for i, spike in enumerate(expected_spikes):
            self.assertEqual(spikes[i][1], spike)
        self.assertEqual(spikes.shape, (len(spikes), 2))
        for spike in expected_spikes:
            print(spike, v[spike][2], v[spike+1][2])
            self.assertTrue(v[spike][2] > v[spike+1][2])
