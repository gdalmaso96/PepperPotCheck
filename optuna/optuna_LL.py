import sys
sys.path.insert(1, "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/include/")
from BeamData import BeamData
import optuna
import numpy as np
from numpy import sqrt as sqrt
import subprocess
import time
import os
import warnings
start_time = time.time()
warnings.filterwarnings("ignore")

# Bayesian optimiser for log likelihood
# Fits the phase space centroids and longitudinal phase space
# 8 parameters: 4 centroids + 4 parameters of the momentum spectrum parametrization

nTrials = 3
nJobs = 1

G4BL = 'singularity run --bind /data/project/general/muonGroup/simulations/giovanni/:/data/project/general/muonGroup/simulations/giovanni /data/project/general/muonGroup/programs/containers/g4beamline-3.06_3.06.sif /data/project/general/muonGroup/simulations/giovanni/g4bl/bash_g4bl.sh COMMAND'
CONFIGURATION_FILE = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/configurations.yaml"
WORKDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"
CONTAINERDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"
    
# Load BeamData:
DATA = BeamData(CONFIGURATION_FILE, G4BL, WORKDIR, CONTAINERDIR)

names = ['a', 'b', 'c', 'd', 'x', 'xp', 'y', 'yp']

def objective(trial):
    a = trial.suggest_uniform('a', 0.01, 5)
    b = trial.suggest_uniform('b', 25, 35)
    c = trial.suggest_uniform('c', 0.01, 5)
    d = trial.suggest_uniform('d', 0.01, 5)
    x = trial.suggest_uniform('x', -100, 100)
    xp = trial.suggest_uniform('xp', -100, 100)
    y = trial.suggest_uniform('y', -100, 100)
    yp = trial.suggest_uniform('yp', -100, 100)
    beam = [a, b, c, d, x, xp, y, yp]
    
    result0 = DATA.RunTrial(beam, 100000, "out_%d_" %(trial.number), "beam_%d.root" %(trial.number))
    
    return result0

if __name__ == '__main__':
    args = sys.argv[1:]
    
    study = optuna.create_study(study_name="LL", storage='sqlite:////data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/DBs/LL.db', direction='maximize', load_if_exists=True)
    
    study.optimize(objective, n_trials=nTrials, n_jobs=nJobs)

    print("--- %s seconds ---" % (time.time() - start_time))
    

