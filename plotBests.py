import sys
sys.path.insert(1, '/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/include')
from BeamData import BeamData
import time
start_time = time.time()
import matplotlib.pyplot as plt
import optuna
import numpy as np

#data = BeamData("configurations.yaml", "docker exec -ti --workdir=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl g4bl /bin/bash -c 'source /home/developer/.bashrc && g4bl COMMAND'")
data = BeamData("configurations_MEGonly.yaml", "docker exec -ti --workdir=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl g4bl /bin/bash -c 'source /home/developer/.bashrc && g4bl COMMAND'")

#data.PlotBest("newH")
data.PlotBest("bestCentMEGonly")
