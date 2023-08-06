import numpy as np
import pandas as pd
import h5py
from scipy.interpolate import interp1d
import utm
import os
import subprocess
import shutil
import json

## get the absolute path name of the included EQHazard.jar file
import seaturtles
import inspect
EQHazard_file = os.path.dirname(inspect.getfile(seaturtles)) + '\EQHazard.jar'

