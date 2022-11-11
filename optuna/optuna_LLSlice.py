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
from optuna.samplers import NSGAIISampler
start_time = time.time()
warnings.filterwarnings("ignore")

# Bayesian optimiser for log likelihood
# Fits the phase space centroids, longitudinal phase space and the Peper Pot horixontal slice in x = -6.25mm
# 8 parameters: 4 centroids + 4 parameters of the momentum spectrum parametrization + 6 paramters of the slice

nTrials = 1 #3
nJobs = 1
slicex_X = [{'x': -6.25, 'Amin': 2.2, 'Amax': 3.0}]
slicey_Y = []


G4BL = 'singularity run --bind /data/project/general/muonGroup/simulations/giovanni/:/data/project/general/muonGroup/simulations/giovanni /data/project/general/muonGroup/programs/containers/g4beamline-3.06_3.06.sif /data/project/general/muonGroup/simulations/giovanni/g4bl/bash_g4bl.sh COMMAND'
CONFIGURATION_FILE = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/configurations.yaml"
WORKDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"
CONTAINERDIR = "/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/"
	
# Load BeamData:
DATA = BeamData(CONFIGURATION_FILE, G4BL, WORKDIR, CONTAINERDIR)

def objective(trial):
	a = trial.suggest_uniform('a', 0.01, 5)
	b = trial.suggest_uniform('b', 25, 29.79)
	c = trial.suggest_uniform('c', 0.01, 5)
	d = trial.suggest_uniform('d', 0.01, 5)
	#a = 0.0812462
	#b = 27.8995
	#c = 1.23719
	#d = 0.05
	megx = trial.suggest_uniform('megx', -100, 100)
	megxp = trial.suggest_uniform('megxp', -500, 500)
	mu3ex = trial.suggest_uniform('mu3ex', -100, 100)
	mu3exp = trial.suggest_uniform('mu3exp', -500, 500)
	y = trial.suggest_uniform('y', -100, 100)
	yp = trial.suggest_uniform('yp', -500, 500)
	beam = [a, b, c, d, megx, megxp, mu3ex, mu3exp, y, yp]

	slicex = []
	for X in slicex_X:
		temp = {}
		temp['x'] = X['x']
		temp['A'] = trial.suggest_uniform('A_x%d' %(len(slicex)), X['Amin'], X['Amax'])
		temp['mu'] = trial.suggest_uniform('mu_x%d' %(len(slicex)), -30, 30)
		temp['s1'] = trial.suggest_uniform('s1_x%d' %(len(slicex)), 40, 90)
		temp['l1'] = trial.suggest_uniform('l1_x%d' %(len(slicex)), -20, 20)
		temp['s2'] = trial.suggest_uniform('s2_x%d' %(len(slicex)), 40, 90)
		temp['l2'] = trial.suggest_uniform('l2_x%d' %(len(slicex)), -20, 20)
		slicex.append(temp)
	
	slicey = []
	for Y in slicey_Y:
		temp = {}
		temp['y'] = Y['y']
		temp['A'] = trial.suggest_uniform('A_y%d' %(len(slicey)), Y['Amin'], Y['Amax'])
		temp['mu'] = trial.suggest_uniform('mu_y%d' %(len(slicey)), -50, 10)
		temp['s1'] = trial.suggest_uniform('s1_y%d' %(len(slicey)), 40, 80)
		temp['l1'] = trial.suggest_uniform('l1_y%d' %(len(slicey)), -10, 30)
		temp['s2'] = trial.suggest_uniform('s2_y%d' %(len(slicey)), 40, 80)
		temp['l2'] = trial.suggest_uniform('l2_y%d' %(len(slicey)), -20, 10)
	
	beam = {'beam': beam, 'slicex': slicex, 'slicey': slicey}
	result0 = DATA.RunTrialSlice(beam, 100000, "out_%d_" %(trial.number), "beam_%d" %(trial.number)) #, False)
	
	return result0

if __name__ == '__main__':
	args = sys.argv[1:]
	
	sampler = NSGAIISampler(population_size=50)
	storage = optuna.storages.RDBStorage(url='sqlite:////data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/DBs/LLSlice.db', engine_kwargs={"connect_args": {"timeout": 1000}})
	study = optuna.create_study(study_name="LLSlice", storage=storage, sampler=sampler, direction='minimize', load_if_exists=True)
	if len(args) == 1:
		firstTry = {'a' : 0.0812462, 'b' : 27.8995, 'c' : 1.23719, 'd' : 0.05, 'megx' : 0, 'megxp' : 0, 'mu3ex' : 0, 'mu3exp' : 0, 'y' : 0, 'yp' : 0, 'A_x0' : 2.4, 'mu_x0' : -1, 's1_x0' : 72, 'l1_x0' : 0, 's2_x0' : 83, 'l2_x0' : -9}
		study.enqueue_trial(firstTry)
	
	study.optimize(objective, n_trials=nTrials, n_jobs=nJobs)

	while(time.time() -start_time < 1200):
		study.optimize(objective, n_trials=nTrials, n_jobs=nJobs)

	print("--- %s seconds ---" % (time.time() - start_time))
	

