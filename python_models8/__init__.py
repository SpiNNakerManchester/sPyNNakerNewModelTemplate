from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
from python_models8 import model_binaries

import os

# This adds the model binaries path to the paths searched by sPyNNaker
AbstractSpiNNakerCommon.register_binary_search_path(
    os.path.dirname(model_binaries.__file__))
