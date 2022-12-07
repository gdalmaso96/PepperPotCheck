# Add method to run pepper-pot reconstruction as well, so that the full analysis is self-contained in the repo and future analysis can be run automatically by only changing the txt files from the PILL detectors.
# Need to avoid negative interpolations

import yaml
import subprocess
from scipy.interpolate import interp1d, interp2d, RectBivariateSpline
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import optuna
import uproot
from scipy.optimize import curve_fit
import os

class BeamData:
	def __init__(self, configurationFile, g4bl = "docker exec -ti --workDir=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl g4bl /bin/bash -c 'source /home/developer/.bashrc && g4bl COMMAND'", workDir = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/", containerDir = "/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/"):
		with open(configurationFile) as f:
			data = yaml.load(f, Loader=yaml.FullLoader)
		self.datasets = data['datasets']
		self.simulations = data['simulations']
		self.pepperpot = data['pepperpot']

		# Initialise likelihoods:
		#  -> evaluate likelyhood using python only (if too slow switch to ROOT)
		self.initializeLL()

		# Initialise complessive likelyhood
		self.LL = 0

		# Initialise complessive chi quares
		self.Chi2 = 0

		# Set g4bl command
		self.g4bl = g4bl
	
		# Set work directory path
		self.workDir = workDir

		# Set container folder, on cluster it corresponds to workDir
		self.containerDir = containerDir

		# Set to 1 if you want to sample the 5d phase space correlation matrix
		self.FreeCorrelations = 0

	divertOutput = 0
	
	# General functions
	def surface(self, x):
		return 1e5*(np.abs(x)/29.79)**3.5*(x>0)*(x<29.79)
	
	def gaus(self, x, a, mu, s):
		return a*np.exp(-(x-mu)**2/2./s**2)
	
	def getGausPars(self, x, y, side):
		tmpMu = (y*x).sum()/y.sum()
		tmpSleft  = np.sqrt((y*(x-tmpMu)**2*(x<tmpMu)).sum()/(y*(x<tmpMu)).sum())
		tmpSright = np.sqrt((y*(x-tmpMu)**2*(x>tmpMu)).sum()/(y*(x>tmpMu)).sum())
		
		# Fit tail to 0 n.d.o.f.
		if side == 'left':
			popt, pcov = curve_fit(self.gaus, [x[0], x[1], x[2]], [y[0], y[1], y[2]], p0=[y.max(), tmpMu, tmpSleft], bounds = [[y.max()*0.8, x[0], tmpSleft*0.8], [y.max()*1.2, x[-1], tmpSleft*1.2]])
		elif side == 'right':
			popt, pcov = curve_fit(self.gaus, [x[-1], x[-2], x[-3]], [y[-1], y[-2], y[-3]], p0=[y.max(), tmpMu, tmpSright], bounds = [[y.max()*0.8, x[0], tmpSright*0.8], [y.max()*1.2, x[-1], tmpSright*1.2]])
		return popt
	
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
							profDict = {'profile' : profile, 'dProfile' : np.sqrt(profile[1]*2000)/2000, 'direction' : 'y', 'run' : data['Simulation n.']}
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
							profDict = {'profile' : profile, 'dProfile' : np.sqrt(profile[1]*2000)/2000, 'direction' : 'x', 'run' : data['Simulation n.']}
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
						profDict = {'profile' : profileX, 'dProfile' : np.sqrt(profileX[1]*2000)/2000, 'direction' : 'x', 'run' : data['Simulation n.']}
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
						profDict = {'profile' : profileY, 'dProfile' : np.sqrt(profileY[1]*2000)/2000, 'direction' : 'y', 'run' : data['Simulation n.']}
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
					profDict = {'profile' : profile, 'dProfile' : np.sqrt(profile[2]*2000)/2000, 'direction' : 'xy', 'run' : data['Simulation n.']}
					profDict = self.InitInterp(profDict)
					data['profileLL'].append(profDict)
					profilesLL.append(profDict)
	
	def SetFreeCorrelations(self, boolean):
		self.FreeCorrelations = boolean
	
	def CreateCorrelation(self, tanhs, order):
		# Method found in https://mc-stan.org/docs/2_26/reference-manual/correlation-matrix-transform-section.html
		# Create z
		z = np.zeros((order, order))
		z[np.triu_indices(order, k=1)] = tanhs
		print("Relative correlations:")
		print(z)

		# Create Cholesky
		w = np.zeros((order, order))
		for i in range(order):
			for j in range(order):
				if (i > j):
					w[i,j] = 0
				elif (i == 0 and j == 0):
					w[i,j] = 1
				elif (0 < i and i == j):
					w[i,j] = 1
					for i1 in range(0, i):
						w[i,j] = w[i,j]*(1-z[i1,j]**2)**0.5
				elif (i == 0 and i < j):
					w[i,j] = z[i,j]
				elif (0 < i and i < j):
					w[i,j] = z[i,j]
					for i1 in range(0, i):
						w[i,j] = w[i,j]*(1-z[i1,j]**2)**0.5

		x = w.transpose().dot(w)
		print("Correlation matrix: yp, y, xp, x, P:")
		print(x)
		return x

	# This function introduces correlation between two vectors of data through Iman-Cover method
	# At the moment the the transverse correlation matrix is fully sampled, while the only non-zero correlation on the momentum is with x
	def ImanConover(self, x, xp, y, yp, Ptot, rhoxxp, rhoxy, rhoyyp, rhoxpy, rhoxyp, rhoxpyp, rhoxP):
		x1 = yp
		x2 = y
		x3 = xp
		x4 = x
		x5 = Ptot
		N = len(x1)
		# Sample gauss
		r1 = np.random.normal(0,1,N)
		r2 = np.random.normal(0,1,N)
		r3 = np.random.normal(0,1,N)
		r4 = np.random.normal(0,1,N)
		r5 = np.random.normal(0,1,N)

		# Build matrix
		sigma = self.CreateCorrelation([rhoyyp, rhoxpyp, rhoxyp, 0, rhoxpy, rhoxy, 0, rhoxxp, 0, rhoxP], 5)
		
		L = np.linalg.cholesky(sigma)

		# Introduce correlation
		r1, r2, r3, r4, r5 = np.matmul(L, np.array([r1,r2,r3,r4,r5]))

		# Get sort index
		i1 = np.argsort(r1)
		i2 = np.argsort(r2)
		i3 = np.argsort(r3)
		i4 = np.argsort(r4)
		i5 = np.argsort(r5)
		ix1 = np.argsort(x1)
		ix2 = np.argsort(x2)
		ix3 = np.argsort(x3)
		ix4 = np.argsort(x4)
		ix5 = np.argsort(x5)

		# Ordered vectors
		x1 = x1[ix1]
		x2 = x2[ix2]
		x3 = x3[ix3]
		x4 = x4[ix4]
		x5 = x5[ix5]

		# Rank
		I1 = np.argsort(i1)
		x1 = x1[I1]
		I2 = np.argsort(i2)
		x2 = x2[I2]
		I3 = np.argsort(i3)
		x3 = x3[I3]
		I4 = np.argsort(i4)
		x4 = x4[I4]
		I5 = np.argsort(i5)
		x5 = x5[I5]

		return x4, x3, x2, x1, x5 # yp, y, xp, x, P

	
	# Slice function
	def sliceFunction(self, x, pepperpot):
		A = pepperpot['A']
		mu = pepperpot['mu']
		s1 = pepperpot['s1']
		l1 = pepperpot['l1']
		s2 = pepperpot['s2']
		l2 = pepperpot['l2']
		return A*((x < mu)*(np.exp(-(x-mu)**2/(s1**2+np.abs(l1*(x-mu))))) + (x > mu)*(np.exp(-(x-mu)**2/(s1**2+np.abs(l1*(x-mu))))))
	
	# Prepare 2d cumulative function with gaussian tails
	# Takes as an argument a list of slice parameters to then sample the transverse phase space
	# The idea is that it is not directly dependent on the data to make it easier to add any number of slices
	def prepare2dCumulative(self, pepperpot, key, scale=1):
		y = np.linspace(-500, 500, 100)
		x = []
		# Add one slice at the begining to set 0 boundary conditions
		x.append(pepperpot[0][key] - (pepperpot[1][key] - pepperpot[0][key]))
		for i in range(len(pepperpot)):
			x.append(pepperpot[i][key])
		# Add one slice at the end to set 0 boundary conditions
		x.append(pepperpot[-1][key] + (pepperpot[-1][key] - pepperpot[-2][key]))

		X = []
		for i in range(len(y)):
			X.append(x)
		X = np.array(X)

		Y = []
		for i in range(len(x)):
			Y.append(y)
		Y = np.transpose(Y)

		Z = []
		# Add zero values on the boundaries in the space direction
		Z.append(np.zeros(len(y)))
		for i in range(len(pepperpot)):
			Z.append(self.sliceFunction(y*scale, pepperpot[i]))
		Z.append(np.zeros(len(y)))
		Z = np.array(Z)

		# Interpolate
		f = RectBivariateSpline(x, y, Z, kx=3, ky=3)
		x = np.linspace(x[1], x[-2], 50)
		y = np.linspace(-300, 300, 50)

		Z = f(x,y)
		Z = Z*(Z>0)
		# RectBivariateSpline has a strange indexing
		Z = np.transpose(Z)
		X, Y = np.meshgrid(x, y)
		xtot = []
		ytot = []
		ztot = []
		for (x, y, z) in zip(X, Y, Z):
			a, mu, s = self.getGausPars(x, z, 'right')
			tailXright = np.linspace(x[-1] + (x[1]-x[0]), x[-1] + (x[1]-x[0])*30, 30)
			tailYright = np.zeros(30) + y[0]
			tailZright = self.gaus(tailXright, a, mu, s)
			a, mu, s = self.getGausPars(x, z, 'left')
			tailXleft = np.linspace(x[0] - (x[1]-x[0])*30, x[0] - (x[1]-x[0]), 30)
			tailYleft = np.zeros(30) + y[0]
			tailZleft = self.gaus(tailXleft, a, mu, s)
			xtot.append(np.concatenate((tailXleft, x, tailXright)))
			ytot.append(np.concatenate((tailYleft, y, tailYright)))
			ztot.append(np.concatenate((tailZleft, z, tailZright)))
		xtot = np.array(xtot)
		ytot = np.array(ytot)
		ztot = np.array(ztot)
		Z = ztot.flatten()

		cumulative1d = np.cumsum(Z)
		I = np.linspace(0, len(Z) - 1, len(Z))

		# Remove points with the same value
		while True:
			if(np.abs(cumulative1d[0] - cumulative1d[1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, 0)
				I = np.delete(I, 0)
			else:
				break
		ind = 0
		while True:
			if(np.abs(cumulative1d[ind] - cumulative1d[ind+1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, ind+1)
				I = np.delete(I, ind+1)
			else:
				ind += 1

			if(ind+1 >= len(cumulative1d)):
				break

		cumulative1d = cumulative1d - cumulative1d[0]
		cumulative1d = cumulative1d/cumulative1d[-1]
		dx = xtot[0][1]-xtot[0][0]
		lx = len(xtot[0])
		xmin = xtot[0][0]
		dy = ytot[1][0]-ytot[0][0]
		ly = len(ytot[0])
		ymin = ytot[0][0]
		return cumulative1d, I, dx, lx, xmin, dy, ly, ymin
	
	# Prepare 2d cumulative function without gaussian tails
	# Takes as an argument a list of slice parameters to then sample the transverse phase space
	# The idea is that it is not directly dependent on the data to make it easier to add any number of slices
	def prepare2dCumulativeNoTails(self, pepperpot, key):
		y = np.linspace(-500, 500, 100)
		x = []
		# Add one slice at the begining to set 0 boundary conditions
		x.append(pepperpot[0][key] - (pepperpot[1][key] - pepperpot[0][key]))
		for i in range(len(pepperpot)):
			x.append(pepperpot[i][key])
		# Add one slice at the end to set 0 boundary conditions
		x.append(pepperpot[-1][key] + (pepperpot[-1][key] - pepperpot[-2][key]))

		X = []
		for i in range(len(y)):
			X.append(x)
		X = np.array(X)

		Y = []
		for i in range(len(x)):
			Y.append(y)
		Y = np.transpose(Y)

		Z = []
		# Add zero values on the boundaries in the space direction
		Z.append(np.zeros(len(y)))
		for i in range(len(pepperpot)):
			Z.append(self.sliceFunction(y, pepperpot[i]))
		Z.append(np.zeros(len(y)))
		Z = np.array(Z)

		# Interpolate
		f = RectBivariateSpline(x, y, Z, kx=3, ky=3)
		x = np.linspace(-50, 50, 500)
		y = np.linspace(-300, 300, 500)
		Z = f(x,y)
		# RectBivariateSpline has a strange indexing
		Z = np.transpose(Z)
		Z = Z*(Z>0)
		Z = Z.flatten()

		cumulative1d = np.cumsum(Z)
		I = np.linspace(0, len(Z) - 1, len(Z))

		# Remove points with the same value
		while True:
			if(np.abs(cumulative1d[0] - cumulative1d[1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, 0)
				I = np.delete(I, 0)
			else:
				break
		ind = 0
		while True:
			if(np.abs(cumulative1d[ind] - cumulative1d[ind+1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, ind+1)
				I = np.delete(I, ind+1)
			else:
				ind += 1

			if(ind+1 >= len(cumulative1d)):
				break

		cumulative1d = cumulative1d - cumulative1d[0]
		cumulative1d = cumulative1d/cumulative1d[-1]
		dx = x[1]-x[0]
		lx = len(x)
		xmin = x[0]
		dy = y[1]-y[0]
		ly = len(y)
		ymin = y[0]
		return cumulative1d, I, dx, lx, xmin, dy, ly, ymin
	
	# Prepare the 1d cumulative function 
	# The output array can be used to sample the longitudinal momentum distribution
	# The momentum distribution is modeled as follows:
	#  - surface muon momentum spectrum is assumed to be x**3.5 from 0 to 29.79  (no parameters)
	#  - a gaussian smearing is included to account for cloud muons and energy losses (pars[0] = sigma)
	#  - a gaussian window is applied to account for beamline acceptance up to QSK41 (pars[1] = selected momentum, pars[2] = sigma)
	#  - a gaussian smearing is applied again to take into accaount possible other effects (pars[3] = sigma)
	def prepare1dCumulative(self, pars):
		x = np.linspace(-35, 35, 10000)
		surfacey = self.surface(x)
		surfacey = surfacey/surfacey.max()
		gaussy = self.gaus(x, 1, 0, pars[0])
		
		# First convolution
		surfacey = np.convolve(surfacey, gaussy, "same")
		surfacey = surfacey/surfacey.max()

		# Apply window
		gaussy = self.gaus(x, 1, pars[1], pars[2])
		surfacey = surfacey*gaussy
		surfacey = surfacey/surfacey.max()

		# Second convolution
		gaussy = self.gaus(x, 1, 0, pars[3])
		surfacey = np.convolve(surfacey, gaussy, "same")
		surfacey = surfacey/surfacey.max()
		
		# Build cumulative
		cumulative1d = np.cumsum(surfacey)
		while True:
			if(np.abs(cumulative1d[0] - cumulative1d[1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, 0)
				x = np.delete(x, 0)
			else:
				break

		ind = 0
		while True:
			if(np.abs(cumulative1d[ind] - cumulative1d[ind+1]) < 1e-6):
				cumulative1d = np.delete(cumulative1d, ind+1)
				x = np.delete(x, ind+1)
			else:
				ind += 1

			if(ind+1 >= len(cumulative1d)):
				break

		cumulative1d = cumulative1d - cumulative1d[0]
		cumulative1d = cumulative1d/cumulative1d[-1]
		return cumulative1d, x

	# Sample phase space
	# Beam is a list containing the parameters of the beam to be varied
	# - beam[0-3] = pars in prepare1dCumulative
	# - beam[4] = megx
	# - beam[5] = megxp
	# - beam[6] = mu3ex
	# - beam[7] = mu3exp
	# - beam[8] = y
	# - beam[9] = yp
	# - beam[10] = scaleDiv
	# slicex and slicey are lists with the same structure as BeamData.pepperpot, and contain the info about any additional slice to the pepperpot
	# nEvents is the number of particles to be added to the beam file
	# fileName is the name of the beam output
	# scaleDiv is a scaling factor for the divergences of x and y to take into account the uncertainty on the distance between the PILL and PepperPot plate
	def samplePhaseSpace(self, beam, slicex, slicey, nEvents, fileName):
		# Create the pepperpot list
		pepperpotx = []
		pepperpoty = []
		Ix = 0
		Iy = 0
		for i in range(len(self.pepperpot)):
			if(list(self.pepperpot[i].keys())[-1] == 'x'):
				# Check if slicex or data
				while True:
					if(Ix >= len(slicex)):
						break
					if(slicex[Ix]['x'] >= self.pepperpot[i]['x']):
						break
					if(slicex[Ix]['x'] < self.pepperpot[i]['x']):
						pepperpotx.append(slicex[Ix])
						Ix += 1
				# Add data slice
				pepperpotx.append(self.pepperpot[i])
			elif(list(self.pepperpot[i].keys())[-1] == 'y'):
				# Check if slicex or data
				while True:
					if(Iy >= len(slicey)):
						break
					if(slicey[Iy]['y'] >= self.pepperpot[i]['y']):
						break
					if(slicey[Iy]['y'] < self.pepperpot[i]['y']):
						pepperpoty.append(slicey[Iy])
						Iy += 1
				# Add data slice
				pepperpoty.append(self.pepperpot[i])

		# Sample momentum distribution
		# Create cumulative function: it's fine to do it every time it is sampled. It doesn't take too much time
		print("Interpolate longitudinal")
		cumulative1d, Ptot = self.prepare1dCumulative(beam[0:4])
		
		# Create interpolation
		print("Sample longitudinal")
		f = interp1d(cumulative1d, Ptot, kind='cubic')
		Ptot = f(np.random.rand(nEvents))
		
		# Sample transverse phase space
		# Create horizontal cumulative
		print("Interpolate horizontal")
		cumulative1d, I, dx, lx, xmin, dy, ly, ymin = self.prepare2dCumulative(pepperpotx, 'x', scale=beam[10])
		# Sample horizontal phase space
		print("Sample horizontal")
		fi = interp1d(cumulative1d, I, kind='cubic')
		f = interp1d(I, cumulative1d, kind='cubic')
		r = np.random.rand(nEvents)
		Irand = fi(r)
		dxint = f(Irand.astype(int)+1) - f(Irand.astype(int))
		ddx = dx*(f(Irand) - f(Irand.astype(int)))/dxint
		ddx = ddx*(ddx>0)*(dxint > 0)
		ddy = np.random.rand(nEvents)*dy

		# Need to flip signs on the horizontal as PILL's axis is inverted in MEG configuration
		x = xmin + dx*(Irand.astype(int)%lx) + ddx
		xp = ymin + dy*(Irand.astype(int)/ly) + ddy
		x = -x
		xp = -xp

		# PRINT OUT IRAND IF X OUTSIDE GIVEN RANGE
		# Problems:
		#  1 - when Irand.astype(int)%lx = 499 dx = 100 (to effectively have 500 cells I need 501 points?) <- Should still be ok, would only make the sampling range between -50 and 50.2 mm
		#  2 - cancellation errors: ddx is affected by cancellation. Need a smarter way of doing that -> Maybe after sampling r forget about it and use Irand only? It works
		#for i in range(len(x)):
		#	if abs(x[i]) > 50 or ddx[i] > 1:
		#		print(r[i], Irand[i], xmin, dx, lx, ddx[i])
		#np.save("testx.npy", np.array((cumulative1d, I, x, xp)))


		# Create vertical cumulative
		print("Interpolate vertical")
		cumulative1d, I, dx, lx, xmin, dy, ly, ymin = self.prepare2dCumulative(pepperpoty, 'y', scale=beam[10])
		#np.save("testy.npy", np.array((cumulative1d, I)))
		
		# Sample vertical phase space
		print("Sample vertical")
		fi = interp1d(cumulative1d, I, kind='cubic')
		f = interp1d(I, cumulative1d, kind='cubic')
		r = np.random.rand(nEvents)
		Irand = fi(r)
		Itest1 = (Irand.astype(int))*(Irand.astype(int) > I[0]) + I[0]*(Irand.astype(int) <= I[0])
		Itest2 = (Irand.astype(int)+1)*(Irand.astype(int)+1 < I[-1]) + I[-1]*(Irand.astype(int)+1 >= I[-1])
		dxint = f(Itest2) - f(Itest1)
		dxint = f(Irand.astype(int)+1) - f(Irand.astype(int))
		ddx = dx*(f(Irand) - f(Irand.astype(int)))/dxint
		ddx = ddx*(ddx>0)*(dxint > 0)
		ddy = np.random.rand(nEvents)*dy

		y = xmin + dx*(Irand.astype(int)%lx) + ddx
		yp = ymin + dy*(Irand.astype(int)/ly) + ddy

		# Introduce correlations
		if self.FreeCorrelations == 1:
			x, xp, y, yp, Ptot = self.ImanConover(x, xp, y, yp, Ptot, beam[11], beam[12], beam[13], beam[14], beam[15], beam[16], beam[17])

		# Create beam trees
		print("Create tree")
		xmeg = x + beam[4]
		xpmeg = (xp + beam[5])*1e-3
		xmu3e = x + beam[6]
		xpmu3e = (xp + beam[7])*1e-3
		ytot = y + beam[8]
		yptot = (yp + beam[9])*1e-3

		z = np.zeros(len(x))
		t = np.zeros(len(x))

		Pzmeg = -Ptot/np.sqrt(1 + xpmeg**2 + yptot**2)
		Pxmeg = xpmeg*Pzmeg
		Pymeg = yptot*Pzmeg

		Pzmu3e = -Ptot/np.sqrt(1 + xpmu3e**2 + yptot**2)
		Pxmu3e = xpmu3e*Pzmu3e
		Pymu3e = yptot*Pzmu3e
		
		PDGid = np.zeros(len(x)) - 13
		EventID = np.linspace(1, len(x), len(x))
		TrackID = np.zeros(len(x))
		ParentID = np.zeros(len(x))
		Weight = np.zeros(len(x)) + 1

		# Create file MEG
		fileNameT = self.workDir + '/g4bl/beam/DS' + fileName + 'MEG.root'
		with uproot.recreate(fileNameT) as file:
			tree = {}
			tree['x'] = xmeg.astype('float32')
			tree['y'] = ytot.astype('float32')
			tree['z'] = z.astype('float32')
			tree['Px'] = Pxmeg.astype('float32')
			tree['Py'] = Pymeg.astype('float32')
			tree['Pz'] = Pzmeg.astype('float32')
			tree['t'] = t.astype('float32')
			tree['PDGid'] = PDGid.astype('float32')
			tree['EventID'] = EventID.astype('float32')
			tree['TrackID'] = TrackID.astype('float32')
			tree['ParentID'] = ParentID.astype('float32')
			tree['Weight'] = Weight.astype('float32')

			file['beam'] = tree
			file.close()
		# Convert to tuple
		command =  "root -q -b \"" + self.workDir + "include/convertToNTuple.cpp(\\\"" + fileNameT + "\\\")\""
		subprocess.call(command, shell=True)
		# Create file Mu3e
		fileNameT = self.workDir + '/g4bl/beam/DS' + fileName +'Mu3e.root'
		with uproot.recreate(fileNameT) as file:
			tree = {}
			tree['x'] = xmu3e.astype('float32')
			tree['y'] = ytot.astype('float32')
			tree['z'] = z.astype('float32')
			tree['Px'] = Pxmu3e.astype('float32')
			tree['Py'] = Pymu3e.astype('float32')
			tree['Pz'] = Pzmu3e.astype('float32')
			tree['t'] = t.astype('float32')
			tree['PDGid'] = PDGid.astype('float32')
			tree['EventID'] = EventID.astype('float32')
			tree['TrackID'] = TrackID.astype('float32')
			tree['ParentID'] = ParentID.astype('float32')
			tree['Weight'] = Weight.astype('float32')

			file['beam'] = tree
			file.close()
		# Convert to tuple
		command =  "root -q -b \"" + self.workDir + "include/convertToNTuple.cpp(\\\"" + fileNameT + "\\\")\""
		subprocess.call(command, shell=True)
		return 0
	
	# This method rearranges the points of rasterscans in a grid
	def MakeGrid(self, x, y, z):
		X = []
		Y = []
		Z = []
		nPerRow = 0
		tempY = -100
		for y1 in y:
			if(np.abs(y1-tempY) > 0.2):
				nPerRow += 1
				tempY = y1
		nPerColumn = int(len(y)/nPerRow)
		for i in range(nPerRow):
			X.append(x[i*nPerColumn:(i+1)*nPerColumn])
			Y.append(y[i*nPerColumn:(i+1)*nPerColumn])
			Z.append(z[i*nPerColumn:(i+1)*nPerColumn])
		X = np.array(X)
		Y = np.array(Y)
		Z = np.array(Z)

		return X,Y,Z

	def AddTails(self, X, Y, Z, nPoints = 5):
		xtot = []
		ytot = []
		ztot = []
		#Horizontal tails
		for (x, y, z) in zip(X, Y, Z):
			a, mu, s = self.getGausPars(x, z, 'right')
			tailXright = np.linspace(x[-1] + (x[1]-x[0]), x[-1] + (x[1]-x[0])*nPoints, nPoints)
			tailYright = np.zeros(nPoints) + y[0]
			tailZright = self.gaus(tailXright, a, mu, s)
			a, mu, s = self.getGausPars(x, z, 'left')
			tailXleft = np.linspace(x[0] - (x[1]-x[0])*nPoints, x[0] - (x[1]-x[0]), nPoints)
			tailYleft = np.zeros(nPoints) + y[0]
			tailZleft = self.gaus(tailXleft, a, mu, s)
			xtot.append(np.concatenate((tailXleft, x, tailXright)))
			ytot.append(np.concatenate((tailYleft, y, tailYright)))
			ztot.append(np.concatenate((tailZleft, z, tailZright)))
		
		# Vertical tails
		xtemp = np.transpose(np.array(xtot))
		ytemp = np.transpose(np.array(ytot))
		ztemp = np.transpose(np.array(ztot))
		xtot = []
		ytot = []
		ztot = []
		for (x, y, z) in zip(ytemp, xtemp, ztemp):
			a, mu, s = self.getGausPars(x, z, 'right')
			tailXright = np.linspace(x[-1] + (x[1]-x[0]), x[-1] + (x[1]-x[0])*nPoints, nPoints)
			tailYright = np.zeros(nPoints) + y[0]
			tailZright = self.gaus(tailXright, a, mu, s)
			a, mu, s = self.getGausPars(x, z, 'left')
			tailXleft = np.linspace(x[0] - (x[1]-x[0])*nPoints, x[0] - (x[1]-x[0]), nPoints)
			tailYleft = np.zeros(nPoints) + y[0]
			tailZleft = self.gaus(tailXleft, a, mu, s)
			xtot.append(np.concatenate((tailYleft, y, tailYright)))
			ytot.append(np.concatenate((tailXleft, x, tailXright)))
			ztot.append(np.concatenate((tailZleft, z, tailZright)))
		xtot = np.transpose(np.array(xtot))
		ytot = np.transpose(np.array(ytot))
		ztot = np.transpose(np.array(ztot))
		return xtot, ytot, ztot


		

	# Init interpolation
	def InitInterp(self, profile):
		# if raster scan prepare 2d cubic spline
		if profile['direction'] == 'xy':
			x,y,z = self.MakeGrid(profile['profile'][0], profile['profile'][1], profile['profile'][2])
			x,y,z = self.AddTails(x,y,z, 3)
			f = RectBivariateSpline(y[:,0],x[0],z)
			profile['interpolation'] = f
			# Evaluate normalization once
			profile['norm'] = integrate.dblquad(profile['interpolation'], profile['profile'][0][0], profile['profile'][0][-1], profile['profile'][1][0], profile['profile'][1][-1])[0]
		else:
			f = interp1d(profile['profile'][0], profile['profile'][1], kind='cubic', fill_value=1e-12, bounds_error=False)
			profile['interpolation'] = f
			# Evaluate normalization once
			profile['norm'] = integrate.quad(profile['interpolation'], profile['profile'][0][0], profile['profile'][0][-1])[0]
		return profile
	
	# Evaluate LL
	def EvaluateLL(self, data, histoFile):
		LL = 0
		if data['Beamline'].find('HULK'):
			treeName = 'NTuple/Z10175'
		else:
			treeName = 'VirtualDetector/PILL'

		with uproot.open(histoFile + ':' + treeName) as pill:
			# Cycle over all profilesLL
			for profile in data['profileLL']:
			# Check what kind of profile it is
				if(profile['direction'] == 'x'):
					s = pill.arrays(['x'], '(abs(y) < 1) & (x > %f) & (x < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['x']
					if(data['Beamline'].find('MEG') >= 0):
						s = -s
					# Check if any particle is transmitted
					if(len(s) < 1):
						LL += 1000
					else:
						LL += (-2*np.log(np.abs(profile['interpolation'](s))/profile['norm'])).sum()/len(s)/len(s)
				elif(profile['direction'] == 'y'):
					s = pill.arrays(['y'], '(abs(x) < 1) & (y > %f) & (y < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['y']
					# Check if any particle is transmitted
					if(len(s) < 1):
						LL += 1000
					else:
						LL += (-2*np.log(np.abs(profile['interpolation'](s))/profile['norm'])).sum()/len(s)/len(s)
				elif(profile['direction'] == 'xy'):
					s = pill.arrays(['x', 'y'], library = 'np')
					if data['Beamline'].find('HULK'):
						s['x'] = -s['x']
					for i in range(s['x'].size):
						# Check if any particle is transmitted
						if(s['x'].size < 1):
							LL += 1000
						else:
							LL += (-2*np.log(profile['interpolation'](s['y'][i], s['x'][i])/profile['norm'])).sum()/s['x'].size/s['x'].size
		return LL
	
	# Evaluate Chi2: like with the likelyhood the result is chi2 normalised to the number of particles to favor higher transmission
	# In fact there is no need to include the degrees of freedom at this level: those are constanat for each optimization, so they are meaningful only for significance tests
	def EvaluateChi2Norm(self, data, histoFile):
		Chi2 = 0
		if data['Beamline'].find('HULK'):
			treeName = 'NTuple/Z10175'
		else:
			treeName = 'VirtualDetector/PILL'

		with uproot.open(histoFile + ':' + treeName) as pill:
			# Cycle over all profilesLL
			for profile in data['profileLL']:
			# Check what kind of profile it is
				if(profile['direction'] == 'x'):
					s = pill.arrays(['x'], '(abs(y) < 1) & (x > %f) & (x < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['x']
					if(data['Beamline'].find('MEG') >= 0):
						s = -s
					# Check if any particle is transmitted
					if(len(s) < 1):
						Chi2 += 1e12
					else:
						for (x,y) in zip(profile['profile'][0], profile['profile'][1]/profile['norm']):
							tmp = (np.abs(s-x) < 1).sum()
							y1 = tmp/len(s)/2 # each bin is 2 mm wide
							dy1 = np.sqrt(tmp)/len(s)/2
							#if dy1 > 0:
							#	Chi2 += (y1 - y)**2/dy1**2/len(s)
							#else:
							#	Chi2 += (y1 - y)**2/len(s)
							Chi2 += (y1 - y)**2/len(s)
				elif(profile['direction'] == 'y'):
					s = pill.arrays(['y'], '(abs(x) < 1) & (y > %f) & (y < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['y']
					# Check if any particle is transmitted
					if(len(s) < 1):
						Chi2 += 1e12
					else:
						for (x,y) in zip(profile['profile'][0], profile['profile'][1]/profile['norm']):
							tmp = (np.abs(s-x) < 1).sum()
							y1 = tmp/len(s)/2 # each bin is 2 mm wide
							dy1 = np.sqrt(tmp)/len(s)/2
							#if dy1 > 0:
							#	Chi2 += (y1 - y)**2/dy1**2/len(s)
							#else:
							#	Chi2 += (y1 - y)**2/len(s)
							Chi2 += (y1 - y)**2/len(s)
				elif(profile['direction'] == 'xy'):
					s = pill.arrays(['x', 'y'], library = 'np')
					# Check if any particle is transmitted
					sx = s['x']
					sy = s['y']
					if data['Beamline'].find('HULK'):
						sx = -sx
					if(len(sx) < 1):
						Chi2 += 1e12
					else:
						for (x,y,z) in zip(profile['profile'][0], profile['profile'][1], profile['profile'][2]/profile['norm']):
							tmp = ((np.abs(sx-x) < 1)*(np.abs(sy-y) < 1)).sum()
							z1 = tmp/len(sx)/4 # each bin is 2 mm wide
							dz1 = np.sqrt(tmp)/len(sx)/4
							#if dz1 > 0:
							#	Chi2 += (z1 - z)**2/dz1**2/len(sx)
							#else:
							#	Chi2 += (z1 - z)**2/len(sx)
							Chi2 += (z1 - z)**2/len(sx)
		return Chi2
	# Evaluate Chi2: like with the likelyhood the result is chi2 normalised to the number of particles to favor higher transmission
	# In fact there is no need to include the degrees of freedom at this level: those are constanat for each optimization, so they are meaningful only for significance tests
	def EvaluateChi2(self, data, histoFile):
		Chi2 = 0
		if data['Beamline'].find('HULK'):
			treeName = 'NTuple/Z10175'
		else:
			treeName = 'VirtualDetector/PILL'

		with uproot.open(histoFile + ':' + treeName) as pill:
			# Cycle over all profilesLL
			for profile in data['profileLL']:
			# Check what kind of profile it is
				if(profile['direction'] == 'x'):
					s = pill.arrays(['x'], '(abs(y) < 1) & (x > %f) & (x < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['x']
					if(data['Beamline'].find('MEG') >= 0):
						s = -s
					# Check if any particle is transmitted
					if(len(s) < 100000):
						Chi2 += 1e12
					else:
						for (x,y,dy) in zip(profile['profile'][0], profile['profile'][1]/profile['norm'], profile['dProfile']/profile['norm']):
							tmp = (np.abs(s-x) < 1).sum()
							y1 = tmp/2/len(s) # each bin is 2 mm wide
							dy1 = np.sqrt(tmp)/2/len(s)
							#if dy1 > 0:
							#	Chi2 += (y1 - y)**2/dy1**2/len(s)
							#else:
							#	Chi2 += (y1 - y)**2/len(s)
							Chi2 += (y1 - y)**2/(dy**2+dy1**2)
				elif(profile['direction'] == 'y'):
					s = pill.arrays(['y'], '(abs(x) < 1) & (y > %f) & (y < %f)' %(profile['profile'][0][0], profile['profile'][0][-1]), library = 'np')['y']
					# Check if any particle is transmitted
					if(len(s) < 100000):
						Chi2 += 1e12
					else:
						for (x,y,dy) in zip(profile['profile'][0], profile['profile'][1]/profile['norm'], profile['dProfile']/profile['norm']):
							tmp = (np.abs(s-x) < 1).sum()
							y1 = tmp/2/len(s) # each bin is 2 mm wide
							dy1 = np.sqrt(tmp)/2/len(s)
							#if dy1 > 0:
							#	Chi2 += (y1 - y)**2/dy1**2/len(s)
							#else:
							#	Chi2 += (y1 - y)**2/len(s)
							Chi2 += (y1 - y)**2/(dy**2+dy1**2)
				elif(profile['direction'] == 'xy'):
					s = pill.arrays(['x', 'y'], library = 'np')
					# Check if any particle is transmitted
					sx = s['x']
					sy = s['y']
					if data['Beamline'].find('HULK'):
						sx = -sx
					if(len(sx) < 100000):
						Chi2 += 1e12
					else:
						for (x,y,z,dz) in zip(profile['profile'][0], profile['profile'][1], profile['profile'][2]/profile['norm'], profile['dProfile']/profile['norm']):
							tmp = ((np.abs(sx-x) < 1)*(np.abs(sy-y) < 1)).sum()
							z1 = tmp/4/len(s) # each bin is 2 mm wide
							dz1 = np.sqrt(tmp)/4/len(s)
							#if dz1 > 0:
							#	Chi2 += (z1 - z)**2/dz1**2/len(sx)
							#else:
							#	Chi2 += (z1 - z)**2/len(sx)
							Chi2 += (z1 - z)**2/(dz**2+dz1**2)
		return Chi2
	
	# Run simulation trial for LL evaluation including beam interpolation
	# - beam[0-3] = pars in prepare1dCumulative
	# - beam[4] = megx
	# - beam[5] = megxp
	# - beam[6] = mu3ex
	# - beam[7] = mu3exp
	# - beam[8] = y
	# - beam[9] = yp
	# slicex and slicey are lists with the same structure as BeamData.pepperpot, and contain the info about any additional slice to the pepperpot
	def RunTrialSlice(self, beam, nEvents, histoFile, beamFile, DELETEFILES = True, method = 'LL'):
		# Generate beamfile
		self.samplePhaseSpace(beam['beam'], beam['slicex'], beam['slicey'], nEvents, beamFile)

		# Back propagate
		commandBeam = " " + self.containerDir + "/g4bl/scripts/" + self.simulations['Invert']['Beamline']
		params = self.simulations['Invert'].copy()
		params.pop('Beamline')

		for par in params:
			commandBeam = commandBeam + " " + par + "=%f" %(params[par])
		
		commandBeam = commandBeam + " workDir=" + self.containerDir

		# Set number of particles to be propagated
		commandBeam = commandBeam + " " + "last=%d" %(nEvents)

		# MEG
		# Set beamfile
		beamFileMEG = beamFile + "MEG.root"
		commandBeamMEG = commandBeam + " " + "beamFile=" + self.containerDir + "g4bl/beam/DS" + beamFileMEG

		# Set histoFile
		commandBeamMEG = commandBeamMEG + " " + "histoFile=" + self.containerDir + "g4bl/beam/USI" + beamFileMEG

		# Execute
		print(self.g4bl.replace("COMMAND", commandBeamMEG))
		subprocess.call(self.g4bl.replace("COMMAND", commandBeamMEG), shell=True)
		
		# Mu3e
		# Set beamfile
		beamFileMu3e = beamFile + "Mu3e.root"
		commandBeamMu3e = commandBeam + " " + "beamFile=" + self.containerDir + "g4bl/beam/DS" + beamFileMu3e

		# Set histoFile
		commandBeamMu3e = commandBeamMu3e + " " + "histoFile=" + self.containerDir + "g4bl/beam/USI" + beamFileMu3e

		# Execute
		print(self.g4bl.replace("COMMAND", commandBeamMu3e))
		subprocess.call(self.g4bl.replace("COMMAND", commandBeamMu3e), shell=True)

		# Invert beam MEG
		commandBeam = "root -q -b \"" + self.workDir + "include/genBeam.cpp(\\\"" + self.workDir + "g4bl/beam/" + "USI" + beamFileMEG +  "\\\", \\\"" + self.workDir + "g4bl/beam/" + "US" + beamFileMEG  +  "\\\")\""
		print(commandBeam)
		subprocess.call(commandBeam, shell=True)


		# Invert beam Mu3e
		commandBeam = "root -q -b \"" + self.workDir + "include/genBeam.cpp(\\\"" + self.workDir + "g4bl/beam/" + "USI" + beamFileMu3e +  "\\\", \\\"" + self.workDir + "g4bl/beam/" + "US" + beamFileMu3e  +  "\\\")\""
		print(commandBeam)
		subprocess.call(commandBeam, shell=True)

		test = []
		for data in self.datasets:
			if data[method] == 1:
				command= " " + self.containerDir + "/g4bl/scripts/" + self.simulations[data['Beamline']]


				# Copy dataset and extract g4bl parameters
				# In the future might want to copy and pop while getting information about what simulatio to run
				params = data.copy()
				params.pop('fileName')
				params.pop('Data type - 1')
				params.pop('Data type - 2')
				params.pop('Simulation n.')
				beamLine = params.pop('Beamline')
				params.pop('PILL position')
				params.pop('profileLL')

				for par in params:
					command = command + " " + par + "=%f" %(params[par])
				command = command + " workDir=" + self.containerDir
				
				# Set beamfile
				if(beamLine.find("MEG") >= 0):
					command = command + " " + "beamFile=" + self.containerDir + "g4bl/beam/US" + beamFileMEG
				elif(beamLine.find("Mu3e") >= 0):
					command = command + " " + "beamFile=" + self.containerDir + "g4bl/beam/US" + beamFileMu3e

				# Set number of particles to be propagated
				command = command + " " + "last=%d" %(nEvents)

				# Set histoFile
				command = command + " " + "histoFile=" + self.containerDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]) # ADD suffix for different data sets

				print(self.g4bl.replace("COMMAND", command))
				subprocess.call(self.g4bl.replace("COMMAND", command), shell=True)

				# Evaluate fit
				if method == 'LL':
					test.append(self.EvaluateLL(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."])))
					self.LL += test[-1]
					print("%f\n" %(self.LL))
				elif method == 'Chi2':
					test.append(self.EvaluateChi2(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."])))
					self.Chi2 += test[-1]
					print("%f\n" %(self.Chi2))

				# Remove histoFile
				if DELETEFILES:
					os.remove("" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]))
		
		# Remove beamfile
		if DELETEFILES:
			os.remove("" + self.workDir + "g4bl/beam/US" + beamFileMEG)
			os.remove("" + self.workDir + "g4bl/beam/US" + beamFileMu3e)

		print(test)
		if method == 'LL':
			return self.LL
		elif method == 'Chi2':
			return self.Chi2
		else:
			return -1
	
	# Run simulation trial for LL evaluation
	# Beam parameters are: [0,3] - longitudinal parameters, [4, 7] - centroids
	def RunTrial(self, beam, nEvents, histoFile, beamFile, DELETEFILES = True, method = 'LL'):
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
			if data[method] == 1:
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

				# Evaluate fit
				#self.LL += self.EvaluateLL(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]))
				if method == 'LL':
					test.append(self.EvaluateLL(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."])))
					self.LL += test[-1]
					print("%f\n" %(self.LL))
				elif method == 'Chi2':
					test.append(self.EvaluateChi2(data, "" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."])))
					self.Chi2 += test[-1]
					print("%f\n" %(self.Chi2))

				# Remove histoFile
				if DELETEFILES:
					os.remove("" + self.workDir + "g4bl/scores/" + histoFile + "%03d.root" %(data["Simulation n."]))
		
		# Remove beamfile
		if DELETEFILES:
			os.remove("" + self.workDir + "g4bl/beam/US" + beamFile)

		print(test)
		if method == 'LL':
			return self.LL
		elif method == 'Chi2':
			return self.Chi2
		else:
			return -1

	def RunBestTrial(self, study, nEvents, fileName = "best_", beamName = "bestBeam.root"):
		best = study.best_trial
		beam = []
		for par in best.params:
			beam.append(best.params[par])
		self.RunTrial(beam, nEvents, fileName, beamName, False)
	
	def RunBestTrialSlice(self, study, nEvents, firstPars={}, fileName = "best_", beamName = "bestBeam", method='LL'):
		best = study.best_trial
		beam = []
		slicex = []
		slicey = []
		tempx = {}
		tempx['x'] = -6.25
		tempy = {}
		tempy['y'] = 6.25
		print("ciao")
		for par in best.params:
			print(par)
			if(par.find('_x') >= 0):
				tempx[par[0:par.find('_x')]] = best.params[par]
			elif(par.find('_y') >= 0):
				tempy[par[0:par.find('_y')]] = best.params[par]
			else:
				firstPars[par] = best.params[par]
		beam = [firstPars['a'], firstPars['b'], firstPars['c'], firstPars['d'], firstPars['megx'], firstPars['megxp'], firstPars['mu3ex'], firstPars['mu3exp'], firstPars['y'], firstPars['yp'], firstPars['scale'], firstPars['rho']]
		if(len(tempx) > 1):
			slicex.append(tempx)
		#print(slicex[0])
		if(len(tempy) >1 ):
			slicey.append(tempy)
		beam = {'beam' : beam, 'slicex': slicex, 'slicey': slicey}
		self.RunTrialSlice(beam, nEvents, fileName, beamName, False, method=method)
	
	def RunBestTrialCorr5d(self, study, nEvents, firstPars={}, fileName = "best_", beamName = "bestBeam", method='LL'):
		best = study.best_trial
		beam = []
		slicex = []
		slicey = []
		tempx = {}
		tempx['x'] = -6.25
		tempy = {}
		tempy['y'] = 6.25
		print("ciao")
		for par in best.params:
			print(par)
			if(par.find('_x') >= 0):
				tempx[par[0:par.find('_x')]] = best.params[par]
			elif(par.find('_y') >= 0):
				tempy[par[0:par.find('_y')]] = best.params[par]
			else:
				firstPars[par] = best.params[par]
		beam = [firstPars['a'], firstPars['b'], firstPars['c'], firstPars['d'], firstPars['megx'], firstPars['megxp'], firstPars['mu3ex'], firstPars['mu3exp'], firstPars['y'], firstPars['yp'], firstPars['scale'], firstPars['rhoxxp'], firstPars['rhoxy'], firstPars['rhoyyp'], firstPars['rhoxpy'], firstPars['rhoxyp'], firstPars['rhoxpyp'], firstPars['rhoxP']]
		if(len(tempx) > 1):
			slicex.append(tempx)
		#print(slicex[0])
		if(len(tempy) >1 ):
			slicey.append(tempy)
		beam = {'beam' : beam, 'slicex': slicex, 'slicey': slicey}
		self.RunTrialSlice(beam, nEvents, fileName, beamName, False, method=method)
	
	
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
	
	def PlotBest(self, fileName, treeName='VirtualDetector/PILL'):
		# Cycle over data
		for data in self.datasets:
			if data['LL'] == 1:
				# Cycle over all profilesLL
				for profile in data['profileLL']:
					histoFile =  self.workDir + "g4bl/scores/" + fileName + "%03d.root" %(profile['run'])
					with uproot.open(histoFile + ':' + treeName) as pill:
						# Check what kind of profile it is
						if(profile['direction'] == 'x'):
							s = pill.arrays(['x'], 'abs(y) < 1', library = 'np')['x']
							if(data['Beamline'].find('MEG') >= 0):
								s = -s
							
							# Plot
							x = np.linspace(profile['profile'][0][0], profile['profile'][0][-1], 1000)
							y = profile['interpolation'](x)/profile['norm']
							
							plt.plot(x, y, label='Data', color=cm.coolwarm(0))
							plt.hist(s, density=True, range=(profile['profile'][0][0], profile['profile'][0][-1]), bins=100, color=cm.coolwarm(0.9), alpha=0.4, label='Simulation')
							plt.hist(s, density=True, range=(profile['profile'][0][0], profile['profile'][0][-1]), bins=100, color=cm.coolwarm(0.9), histtype='step')
							plt.xlabel("x [mm]")
							plt.legend()
							plt.savefig(histoFile.replace(".root", "_x.png"))
							plt.clf()
		
						elif(profile['direction'] == 'y'):
							s = pill.arrays(['y'], 'abs(x) < 1', library = 'np')['y']
							
							# Plot
							x = np.linspace(profile['profile'][0][0], profile['profile'][0][-1], 1000)
							y = profile['interpolation'](x)/profile['norm']
							
							plt.plot(x, y, label='Data', color=cm.coolwarm(0))
							plt.hist(s, density=True, range=(profile['profile'][0][0], profile['profile'][0][-1]), bins=100, color=cm.coolwarm(0.9), alpha=0.4, label='Simulation')
							plt.hist(s, density=True, range=(profile['profile'][0][0], profile['profile'][0][-1]), bins=100, color=cm.coolwarm(0.9), histtype='step')
							plt.xlabel("y [mm]")
							plt.legend()
							plt.savefig(histoFile.replace(".root", "_y.png"))
							plt.clf()
						elif(profile['direction'] == 'xy'):
							s = pill.arrays(['x', 'y'], library = 'np')
							s['x'] = -s['x']
							
							# Plot
							x,y,z = self.MakeGrid(profile['profile'][0], profile['profile'][1], profile['profile'][2])
							x,y,z = self.AddTails(x,y,z)
							x = np.linspace(x.min(), x.max(), 100)
							y = np.linspace(x.min(), x.max(), 100)
							zIn = profile['interpolation'](y, x)/profile['norm']
							x, y = np.meshgrid(x,y)
							dx = x[0][1] - x[0][0]
							dy = y[1][0] - y[0][0]
							zIn_x = zIn.sum(0)*dx # x integral
							zIn_y = zIn.sum(1)*dy # y integral
							
							fig = plt.figure(figsize=[10,10], dpi=150)
							ax = fig.add_subplot(221)
							plt.title("Data")
							plt.pcolormesh(x,y,zIn, cmap=cm.coolwarm)
							plt.xlabel("x [mm]")
							plt.ylabel("y [mm]")
							plt.xlim(x.min(), x.max())
							plt.ylim(y.min(), y.max())

							ax = fig.add_subplot(222)
							plt.title("Fit")
							plt.hist2d(s['x'], s['y'], bins=[100,100], cmap=cm.coolwarm)
							plt.xlabel("x [mm]")
							plt.ylabel("y [mm]")
							plt.xlim(x.min(), x.max())
							plt.ylim(y.min(), y.max())

							ax = fig.add_subplot(223)
							plt.title("Marginal x distribution")
							plt.plot(x[0], zIn_x, '-', color=cm.coolwarm(0), label='Data')
							plt.hist(s['x'], bins=100, color=cm.coolwarm(0.9), alpha=0.4, density=True, label='Simulation')
							plt.hist(s['x'], bins=100, color=cm.coolwarm(0.9), histtype='step', density=True)
							plt.xlabel("x [mm]")
							plt.xlim(x[0].min(), x[0].max())
							plt.legend()

							ax = fig.add_subplot(224)
							plt.title("Marginal y distribution")
							plt.plot(y[:, 0], zIn_y, '-', color=cm.coolwarm(0), label='Data')
							plt.hist(s['y'], bins=100, color=cm.coolwarm(0.9), alpha=0.4, density=True, label='Simulation')
							plt.hist(s['y'], bins=100, color=cm.coolwarm(0.9), histtype='step', density=True)
							plt.xlabel("y [mm]")
							plt.xlim(y.min(), y.max())
							plt.legend()

							plt.savefig(histoFile.replace(".root", "_xy.png"))
							plt.clf()
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
