# Add method to run pepper-pot reconstruction as well, so that the full analysis is self-contained in the repo and future analysis can be run automatically by only changing the txt files from the PILL detectors.
# Need to avoid negative interpolations

import yaml
import subprocess
from scipy.interpolate import interp1d, interp2d
from scipy import integrate
import numpy as np
import uproot
import os

class BeamData:
	def __init__(self, configurationFile, g4bl = "docker exec -ti --workDir=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl g4bl /bin/bash -c 'source /home/developer/.bashrc && g4bl COMMAND'", workDir = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/", containerDir = "/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/"):
		with open(configurationFile) as f:
			data = yaml.load(f, Loader=yaml.FullLoader)
		self.datasets = data['datasets']
		self.simulations = data['simulations']

		# Initialise likelihoods:
		#  -> evaluate likelyhood using python only (if too slow switch to ROOT)
		self.initializeLL()

		# Initialise complessive likelyhood
		self.LL = 0

		# Set g4bl command
		self.g4bl = g4bl
	
		# Set work directory path
		self.workDir = workDir

		# Set container folder, on cluster it corresponds to workDir
		self.containerDir = containerDir

	divertOutput = 0
	
	# List of likelyhood splines
	def initializeLL(self):
		profilesLL = []
		for data in self.datasets:
			# Check if the data set is used as likelyhood
			if(data["LL"] == 1):
				# Here assume PILL format
				#  - 0: x
				#  - 1: y
				#  - 2: beam
				#  - 4: ch0n
				profile = np.loadtxt(data['fileName'], unpack=True, skiprows=1)
				data['profileLL'] = []
				# Split profile in x and y

				# Tomography data
				if(data["Data type - 1"] == "Tomography"):
					if data["Data type - 2"] == "vertical":
						while(abs(profile[1, 0]) < 0.1):
							profile = np.delete(profile, 0, 1)
						# Remove every row but coodinate and ch0n
						if len(profile[0]) > 4:
							profile = np.delete(profile, 8, 0)
							profile = np.delete(profile, 7, 0)
							profile = np.delete(profile, 6, 0)
							profile = np.delete(profile, 5, 0)
							profile = np.delete(profile, 3, 0)
							profile = np.delete(profile, 2, 0)
							profile = np.delete(profile, 0, 0)
							profDict = {'profile' : profile, 'direction' : 'y'}
							profDict = self.InitInterp(profDict)
							data['profileLL'].append(profDict)
							profilesLL.append(profDict)
					else:
						while(abs(profile[0, -1]) < 0.1):
							profile = np.delete(profile, -1, 1)
						if len(profile[0]) > 4:
							profile = np.delete(profile, 8, 0)
							profile = np.delete(profile, 7, 0)
							profile = np.delete(profile, 6, 0)
							profile = np.delete(profile, 5, 0)
							profile = np.delete(profile, 3, 0)
							profile = np.delete(profile, 2, 0)
							profile = np.delete(profile, 1, 0)
							profDict = {'profile' : profile, 'direction' : 'x'}
							profDict = self.InitInterp(profDict)
							data['profileLL'].append(profDict)
							profilesLL.append(profDict)
				# Quadrupole scan data
				elif(data["Data type - 1"] == "QuadScan"):
					profileX = profile
					profileY = profile
					# Horizontal
					while(abs(profileX[0, -1]) < 0.1):
						profileX = np.delete(profileX, -1, 1)
					if len(profileX[0]) > 4:
						profileX = np.delete(profileX, 8, 0)
						profileX = np.delete(profileX, 7, 0)
						profileX = np.delete(profileX, 6, 0)
						profileX = np.delete(profileX, 5, 0)
						profileX = np.delete(profileX, 3, 0)
						profileX = np.delete(profileX, 2, 0)
						profileX = np.delete(profileX, 1, 0)
						profDict = {'profile' : profileX, 'direction' : 'x'}
						profDict = self.InitInterp(profDict)
						data['profileLL'].append(profDict)
						profilesLL.append(profDict)
					while(abs(profileY[1, 0]) < 0.1):
						profileY = np.delete(profileY, 0, 1)
					# Remove every row but coodinate and ch0n
					if(len(profileY[0]) > 4):
						profileY = np.delete(profileY, 8, 0)
						profileY = np.delete(profileY, 7, 0)
						profileY = np.delete(profileY, 6, 0)
						profileY = np.delete(profileY, 5, 0)
						profileY = np.delete(profileY, 3, 0)
						profileY = np.delete(profileY, 2, 0)
						profileY = np.delete(profileY, 0, 0)
						profDict = {'profile' : profileY, 'direction' : 'y'}
						profDict = self.InitInterp(profDict)
						data['profileLL'].append(profDict)
						profilesLL.append(profDict)

				# Raster scan
				elif(data["Data type - 1"] == "RasterScan"):
					# Remove every row but coordinates and ch0n
					profile = np.delete(profile, 8, 0)
					profile = np.delete(profile, 7, 0)
					profile = np.delete(profile, 6, 0)
					profile = np.delete(profile, 5, 0)
					profile = np.delete(profile, 3, 0)
					profile = np.delete(profile, 2, 0)
					profDict = {'profile' : profile, 'direction' : 'xy'}
					profDict = self.InitInterp(profDict)
					data['profileLL'].append(profDict)
					profilesLL.append(profDict)

	# Init interpolation
	def InitInterp(self, profile):
		# if raster scan prepare 2d cubic spline
		if profile['direction'] == 'xy':
			f = interp2d(profile['profile'][0], profile['profile'][1], profile['profile'][2], kind='cubic', fill_value=1e-12)
			profile['interpolation'] = f
			# Evaluate normalization once
			profile['norm'] = integrate.dblquad(profile['interpolation'], profile['profile'][0][0], profile['profile'][0][-1], profile['profile'][1][0], profile['profile'][1][-1])[0]
		else:
			f = interp1d(profile['profile'][0], profile['profile'][1], kind='cubic', fill_value=1e-12)
			profile['interpolation'] = f
			# Evaluate normalization once
			profile['norm'] = integrate.quad(profile['interpolation'], profile['profile'][0][0], profile['profile'][0][-1])[0]
		return profile
	
	# Evaluate LL
	def EvaluateLL(self, data, histoFile):
		LL = 0
		with uproot.open(histoFile + ":VirtualDetector/PILL") as pill:
			# Cycle over all profilesLL
			for profile in data['profileLL']:
			# Check what kind of profile it is
				if(profile['direction'] == 'x'):
					s = pill.arrays(['x'], 'abs(y) < 1', library = 'np')['x']
					if(data['Beamline'] == 'MEG'):
						s = -s
					LL += (-2*np.log(profile['interpolation'](s)/profile['norm'])).sum()/len(s)
				elif(profile['direction'] == 'y'):
					s = pill.arrays(['y'], 'abs(x) < 1', library = 'np')['y']
					LL += (-2*np.log(profile['interpolation'](s)/profile['norm'])).sum()/len(s)
				elif(profile['direction'] == 'xy'):
					s = pill.arrays(['x', 'y'], library = 'np')
					for i in range(s['x'].size):
						if(data['Beamline'] == 'MEGCOBRA'):
							LL += (-2*np.log(profile['interpolation'](-s['x'][i], s['y'][i])/profile['norm'])).sum()/s['x'].size
						else:
							LL += (-2*np.log(profile['interpolation'](s['x'][i], s['y'][i])/profile['norm'])).sum()/s['x'].size
		return LL
	
	# Run simulation trial for LL evaluation
	# Beam parameters are: [0,3] - longitudinal parameters, [4, 7] - centroids
	def RunTrial(self, beam, nEvents, histoFile, beamFile):
		# Generate beamfile
		commandBeam = "root -q -b \"" + self.workDir + "include/genBeam.cpp(\\\"" + self.workDir + "g4bl/beam/" + "DS" + beamFile +  "\\\", %f, %f, %f, %f, %f, %f, %f, %f, %d," %(beam[0], beam[1], beam[2], beam[3], beam[4], beam[5], beam[6], beam[7], nEvents) + "\\\"" + self.workDir + "g4bl/PepperPotPhaseSpace.root\\\")\""
		print(commandBeam)
		subprocess.call(commandBeam, shell=True)

		# Back propagate
		commandBeam = " " + self.containerDir + "/g4bl/scripts/" + self.simulations['Invert']['Beamline']
		params = self.simulations['Invert'].copy()
		params.pop('Beamline')

		for par in params:
			commandBeam = commandBeam + " " + par + "=%f" %(params[par])
		
		commandBeam = commandBeam + " workDir=" + self.containerDir

		# Set beamfile
		commandBeam = commandBeam + " " + "beamFile=" + self.containerDir + "g4bl/beam/DS" + beamFile
		# Set number of particles to be propagated
		commandBeam = commandBeam + " " + "last=%d" %(nEvents)

		# Set histoFile
		commandBeam = commandBeam + " " + "histoFile=" + self.containerDir + "g4bl/beam/USI" + beamFile

		# Execute
		print(self.g4bl.replace("COMMAND", commandBeam))
		subprocess.call(self.g4bl.replace("COMMAND", commandBeam), shell=True)

		# Invert beam
		commandBeam = "root -q -b \"" + self.workDir + "include/genBeam.cpp(\\\"" + self.workDir + "g4bl/beam/" + "USI" + beamFile +  "\\\", \\\"" + self.workDir + "g4bl/beam/" + "US" + beamFile  +  "\\\")\""
		print(commandBeam)
		subprocess.call(commandBeam, shell=True)

		test = []
		for data in self.datasets:
			if data['LL'] == 1:
				command= " " + self.containerDir + "/g4bl/scripts/" + self.simulations[data['Beamline']]


				# Copy dataset and extract g4bl parameters
                                # In the future might want to copy and pop while getting information about what simulatio to run
				params = data.copy()
				params.pop('fileName')
				params.pop('Data type - 1')
				params.pop('Data type - 2')
				params.pop('Simulation n.')
				params.pop('Beamline')
				params.pop('PILL position')
				params.pop('profileLL')

				for par in params:
					command = command + " " + par + "=%f" %(params[par])
				command = command + " workDir=" + self.containerDir
				
				# Set beamfile
				command = command + " " + "beamFile=" + self.containerDir + "g4bl/beam/US" + beamFile

				# Set number of particles to be propagated
				command = command + " " + "last=%d" %(nEvents)

				# Set histoFile
				command = command + " " + "histoFile=" + self.containerDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]) # ADD suffix for different data sets

				print(self.g4bl.replace("COMMAND", command))
				subprocess.call(self.g4bl.replace("COMMAND", command), shell=True)

				# Evaluate LL
				#self.LL += self.EvaluateLL(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]))
				test.append(self.EvaluateLL(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."])))
				self.LL += test[-1]
				print("%f\n" %(self.LL))

				# Remove histoFile
				os.remove("" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]))
		
		# Remove beamfile
		os.remove("" + self.workDir + "g4bl/beam/US" + beamFile)

		print(test)
		return self.LL


	
	# Run simulation with default settings
	def RunSimulation(self, run, nEvents):
		# Find wanted run
		for data in self.datasets:
			if data['Simulation n.'] == run:
				# Set simulation script
				command= " " + self.containerDir + "/g4bl/scripts/" + self.simulations[data['Beamline']]
				
				# Copy dataset and extract g4bl parameters
				# In the future might want to copy and pop while getting information about what simulatio to run
				params = data.copy()
				params.pop('fileName')
				params.pop('Data type - 1')
				params.pop('Data type - 2')
				params.pop('Simulation n.')
				params.pop('Beamline')
				params.pop('PILL position')

				for par in params:
					command = command + " " + par + "=%f" %(params[par])
				command = command + " workDir=" + self.containerDir

				# Set beamfile
				command = command + " " + "beamFile=" + self.containerDir + "g4bl/beam/" + self.simulations['USbeam']

				# Set number of particles to be propagated
				command = command + " " + "last=%d" %(nEvents)
				
				# Set histoFile
				command = command + " " + "histoFile=" + self.containerDir + "g4bl/scores/" + data['Beamline'] + "_run%05d.root" %(run)

				
				# Run command
				print(self.g4bl.replace("COMMAND", command))
				if(self.divertOutput == 1):
					output = open("" + self.workDir + "g4bl/out/" + data['Beamline'] + "_run%05d.out" %(run), "w+")
					subprocess.call(self.g4bl.replace("COMMAND", command), shell=True, stdout = output)
					output.close()
				else:
					subprocess.call(self.g4bl.replace("COMMAND", command), shell=True)
		return 0
	def PlotComparison(self, run):
		# Find wanted run
		for data in self.datasets:
			if data['Simulation n.'] == run:
				# Set command to run plotComparison.cpp
				command = "root -q -b \"" + self.workDir + "include/plotComparison.cpp(\\\"" + self.workDir + data['fileName'] + "\\\", \\\"" + "" + self.workDir + "g4bl/scores/" + data['Beamline'] + "_run%05d.root" %(run) +  "\\\", 1)\""

				# Run command
				print(command)
				subprocess.call(command, shell=True)
		return 0
