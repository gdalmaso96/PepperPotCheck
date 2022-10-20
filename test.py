import sys
sys.path.insert(1, '/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/include')
from BeamData import BeamData
import time
start_time = time.time()
import matplotlib.pyplot as plt
import numpy as np

data = BeamData("configurations.yaml", "docker exec -ti --workdir=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl g4bl /bin/bash -c 'source /home/developer/.bashrc && g4bl COMMAND'")

beam = [0.0812462, 27.8995, 1.23719, 0.05, 0, 0, 0, 0]

a = data.RunTrial(beam, 10000, "newH", "new.root")
'''
for i in range(3, 38):
	try:
		a = data.datasets[i]
		x = np.linspace(-80, 80, 1000)
		plt.plot(x, a['profileLL'][0]['interpolation'](x), a['profileLL'][0]['profile'][0], a['profileLL'][0]['profile'][1], 'r')
		plt.show()
	except:
		#plt.plot(a['profileLL'][0]['profile'][0], a['profileLL'][0]['profile'][1], 'r')
		#plt.show()
		print(data.datasets[i]['Simulation n.'])
'''
print("LL is %f" %(a))

print("--- %s seconds ---" % (time.time() - start_time))
