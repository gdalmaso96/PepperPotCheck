import yaml

# Configuration files are dictionaries keeping stored info about currents and data files
# Files are located w.r.t. PepperPot folder
# Each configuration has a reference number run for g4bl simulations

# ------------------------------------------------------------------------------------ #
# MEG files

datasets = []
# Pepper pot
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot001.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'poszPILL' : 1250+1117-44, 'Data type - 1' : 'PepperPot', 'Data type - 2' : '25 mm center', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot002.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'PepperPot', 'Data type - 2' : '25 mm staggered', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot003.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'PepperPot', 'Data type - 2' : 'blind', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0})

# Tomography
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo00.txt', 'QSK41cur' : 22.14, 'QSK42cur' : -41.64, 'QSK43cur' : 31.00, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 1, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo01.txt', 'QSK41cur' : 20.39, 'QSK42cur' : -41.37, 'QSK43cur' : 33.07, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 2, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo02.txt', 'QSK41cur' : 21.41, 'QSK42cur' : -41.56, 'QSK43cur' : 31.96, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 3, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo03.txt', 'QSK41cur' : 21.04, 'QSK42cur' : -41.51, 'QSK43cur' : 32.39, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 4, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo04.txt', 'QSK41cur' : 22.70, 'QSK42cur' : -41.66, 'QSK43cur' : 30.13, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 5, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo05.txt', 'QSK41cur' : 21.75, 'QSK42cur' : -41.62, 'QSK43cur' : 31.53, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 6, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo06.txt', 'QSK41cur' : 14.64, 'QSK42cur' : -39.13, 'QSK43cur' : 36.47, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 7, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo07.txt', 'QSK41cur' : 16.06, 'QSK42cur' : -39.81, 'QSK43cur' : 35.93, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 8, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo08.txt', 'QSK41cur' : 16.75, 'QSK42cur' : -40.12, 'QSK43cur' : 35.62, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 9, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo09.txt', 'QSK41cur' : 15.82, 'QSK42cur' : -39.71, 'QSK43cur' : 36.05, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 10, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo10.txt', 'QSK41cur' : 15.10, 'QSK42cur' : -39.37, 'QSK43cur' : 36.35, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 11, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo11.txt', 'QSK41cur' : 14.31, 'QSK42cur' : -38.97, 'QSK43cur' : 36.65, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 12, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})

# Tomography normalized
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN00.txt', 'QSK41cur' : 24.10, 'QSK42cur' : -18.97, 'QSK43cur' : -11.78, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 13, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN01.txt', 'QSK41cur' : 25.39, 'QSK42cur' : -24.06, 'QSK43cur' : -8.18, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 14, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN02.txt', 'QSK41cur' : 25.80, 'QSK42cur' : -25.80, 'QSK43cur' : -7.01, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 15, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN03.txt', 'QSK41cur' : 26.15, 'QSK42cur' : -27.26, 'QSK43cur' : -6.05, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 16, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN04.txt', 'QSK41cur' : 26.68, 'QSK42cur' : -29.63, 'QSK43cur' : -4.53, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 17, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN05.txt', 'QSK41cur' : 27.34, 'QSK42cur' : -32.62, 'QSK43cur' : -2.67, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 18, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN06.txt', 'QSK41cur' : -13.32, 'QSK42cur' : -9.45, 'QSK43cur' : 29.57, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 19, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN07.txt', 'QSK41cur' : 7.55, 'QSK42cur' : -34.27, 'QSK43cur' : 35.81, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 20, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN08.txt', 'QSK41cur' : 14.25, 'QSK42cur' : -38.93, 'QSK43cur' : 36.62, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 21, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN09.txt', 'QSK41cur' : 15.31, 'QSK42cur' : -40.13, 'QSK43cur' : 38.95, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 22, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN10.txt', 'QSK41cur' : -6.08, 'QSK42cur' : -21.91, 'QSK43cur' : 38.52, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 23, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN11.txt', 'QSK41cur' : 7.73, 'QSK42cur' : -36.29, 'QSK43cur' : 44.03, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 24, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 1})


# COBRA profile
datasets.append({'fileName' : 'Data_2022_MEG/COBRA/rasterscan.txt', 'QSK41cur' : 18.50, 'QSK42cur' : -44.1, 'QSK43cur' : 43, 'SML41cur' : -25, 'SMH41' : 200, 'SMV41' : 72.5, 'Data type - 1' : 'RasterScan', 'Data type - 2' : 'horizontal', 'Simulation n.' : 25, 'Beamline': 'MEGCOBRA', 'PILL position' : 'COBRA', 'LL' : 1})
 
# ------------------------------------------------------------------------------------ #
# Mu3e files
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_30A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 30, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 26, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_31A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 31, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 27, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_32A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 32, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 28, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_33A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 33, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 29, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_34A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 34, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 30, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_348A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 31, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_35A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 35, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 32, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_36A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 36, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 33, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_37A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 37, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 34, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_38A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 38, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 35, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_39A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 39, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 36, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_40A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 40, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 37, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_41A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 41, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 38, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 1})


# ------------------------------------------------------------------------------------ #
# Simulation settings
simulations = []
simulations = {'USbeam' : 'USbeam.root', 'USbeamName' : 'beam', 'DSbeam' : 'PepperPotPhaseSpace.root', 'DSbeamName' : 'beam', 'MEG' : 'MEGconfiguration.g4bl', 'MEGCOBRA' : 'MEGCOBRAconfiguration.g4bl', 'Mu3e' : 'Mu3econfiguration.g4bl'}

# ------------------------------------------------------------------------------------ #
# Invert beam simulation settings
invert = {'Beamline' : 'MEGconfiguration.g4bl', 'QSK41cur' : -18.1982, 'QSK42cur' : 40.7008, 'QSK43cur' : -34.8, 'SML41cur' : 10, 'beamPositionZ' : 1250+1117-44, 'poszPILL' : 0}
simulations['Invert'] = invert
# ------------------------------------------------------------------------------------ #
# Configurations settingsi
configurations = {'datasets' : datasets, 'simulations' : simulations}

# ------------------------------------------------------------------------------------ #
with open('configurations.yaml', 'w') as f: 
	data = yaml.dump(configurations, f)

