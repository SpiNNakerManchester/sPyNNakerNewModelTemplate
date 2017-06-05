from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
from python_models8 import model_binaries

import os

# This adds the model binaries path to the paths searched by sPyNNaker
# Seems quite an ugly way of doing it, though... ?
executable_finder = AbstractSpiNNakerCommon._EXECUTABLE_FINDER
executable_finder.add_path(os.path.dirname(model_binaries.__file__))
