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

if __name__ == '__main__':
	args = sys.argv[1:]
	I = int(args[0])
	if I == 0:
		data.PlotBest("CentCorr", treeName='NTuple/Z10175')
	elif I == 1:
		data.PlotBest("CentCorrMom", treeName='NTuple/Z10175')
	elif I == 2:
		data.PlotBest("CentMomScaleCorr", treeName='NTuple/Z10175')
	elif I == 3:
		data.PlotBest("SliceCorr", treeName='NTuple/Z10175')
	elif I == 4:
		data.PlotBest("Corr5d", treeName='NTuple/Z10175')
	elif I == 5:
		data.PlotBest("Corr5d_COBRA", treeName='VirtualDetector/PILL')
	elif I == 6:
		data.PlotBest("CorrMom_COBRA", treeName='VirtualDetector/PILL')
	elif I == 7:
		data.PlotBest("CorrMomSlice_COBRA", treeName='VirtualDetector/PILL')
