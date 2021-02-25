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
