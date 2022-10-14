import sys
sys.path.insert(1, '/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/include')
from BeamData import BeamData
from multiprocessing import Process, cpu_count
from multiprocessing.pool import ThreadPool

if __name__ == '__main__':
	nCores = 6
	
	data = BeamData("/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/configurations.yaml")
	data.divertOutput = 0
	shared_process = []
	
	tp = ThreadPool(nCores)
	
	for i in range(26, 39):
		tp.apply_async(data.PlotComparison, (i,))
	tp.close()
	tp.join()


