import sys
sys.path.insert(1, "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/include/")
from BeamData import BeamData
import time
start_time = time.time()
import matplotlib.pyplot as plt
import optuna
import numpy as np

G4BL = 'singularity run --bind /data/project/general/muonGroup/simulations/giovanni/:/data/project/general/muonGroup/simulations/giovanni /data/project/general/muonGroup/programs/containers/g4beamline-3.06_3.06.sif /data/project/general/muonGroup/simulations/giovanni/g4bl/bash_g4bl.sh COMMAND'
CONFIGURATION_FILE = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/configurations.yaml"
WORKDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"
CONTAINERDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"

data = BeamData(CONFIGURATION_FILE, G4BL, WORKDIR, CONTAINERDIR)

data.PlotBest("best_")
