import yaml

# Configuration files are dictionaries keeping stored info about currents and data files
# Files are located w.r.t. PepperPot folder
# Each configuration has a reference number run for g4bl simulations

# ------------------------------------------------------------------------------------ #
# MEG files

datasets = []
# Pepper pot
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot001.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'poszPILL' : 1250+1117-44, 'Data type - 1' : 'PepperPot', 'Data type - 2' : '25 mm center', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot002.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'PepperPot', 'Data type - 2' : '25 mm staggered', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/pepperpot003.txt', 'QSK41cur' : 18.1982, 'QSK42cur' : -40.7008, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'PepperPot', 'Data type - 2' : 'blind', 'Simulation n.' : 0, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})

# Tomography
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo00.txt', 'QSK41cur' : 22.14, 'QSK42cur' : -41.64, 'QSK43cur' : 31.00, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 1, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo01.txt', 'QSK41cur' : 20.39, 'QSK42cur' : -41.37, 'QSK43cur' : 33.07, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 2, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo02.txt', 'QSK41cur' : 21.41, 'QSK42cur' : -41.56, 'QSK43cur' : 31.96, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 3, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo03.txt', 'QSK41cur' : 21.04, 'QSK42cur' : -41.51, 'QSK43cur' : 32.39, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 4, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo04.txt', 'QSK41cur' : 22.70, 'QSK42cur' : -41.66, 'QSK43cur' : 30.13, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 5, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo05.txt', 'QSK41cur' : 21.75, 'QSK42cur' : -41.62, 'QSK43cur' : 31.53, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 6, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo06.txt', 'QSK41cur' : 14.64, 'QSK42cur' : -39.13, 'QSK43cur' : 36.47, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 7, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo07.txt', 'QSK41cur' : 16.06, 'QSK42cur' : -39.81, 'QSK43cur' : 35.93, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 8, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo08.txt', 'QSK41cur' : 16.75, 'QSK42cur' : -40.12, 'QSK43cur' : 35.62, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 9, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo09.txt', 'QSK41cur' : 15.82, 'QSK42cur' : -39.71, 'QSK43cur' : 36.05, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 10, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo10.txt', 'QSK41cur' : 15.10, 'QSK42cur' : -39.37, 'QSK43cur' : 36.35, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 11, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomo11.txt', 'QSK41cur' : 14.31, 'QSK42cur' : -38.97, 'QSK43cur' : 36.65, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 12, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})

# Tomography normalized
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN00.txt', 'QSK41cur' : 24.10, 'QSK42cur' : -18.97, 'QSK43cur' : -11.78, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 13, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN01.txt', 'QSK41cur' : 25.39, 'QSK42cur' : -24.06, 'QSK43cur' : -8.18, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 14, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN02.txt', 'QSK41cur' : 25.80, 'QSK42cur' : -25.80, 'QSK43cur' : -7.01, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 15, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN03.txt', 'QSK41cur' : 26.15, 'QSK42cur' : -27.26, 'QSK43cur' : -6.05, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 16, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN04.txt', 'QSK41cur' : 26.68, 'QSK42cur' : -29.63, 'QSK43cur' : -4.53, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 17, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN05.txt', 'QSK41cur' : 27.34, 'QSK42cur' : -32.62, 'QSK43cur' : -2.67, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'vertical', 'Simulation n.' : 18, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN06.txt', 'QSK41cur' : -13.32, 'QSK42cur' : -9.45, 'QSK43cur' : 29.57, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 19, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN07.txt', 'QSK41cur' : 7.55, 'QSK42cur' : -34.27, 'QSK43cur' : 35.81, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 20, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN08.txt', 'QSK41cur' : 14.25, 'QSK42cur' : -38.93, 'QSK43cur' : 36.62, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 21, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN09.txt', 'QSK41cur' : 15.31, 'QSK42cur' : -40.13, 'QSK43cur' : 38.95, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 22, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN10.txt', 'QSK41cur' : -6.08, 'QSK42cur' : -21.91, 'QSK43cur' : 38.52, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 23, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_MEG/Collimator/tomoN11.txt', 'QSK41cur' : 7.73, 'QSK42cur' : -36.29, 'QSK43cur' : 44.03, 'SML41cur' : 0, 'Data type - 1' : 'Tomography', 'Data type - 2' : 'horizontal', 'Simulation n.' : 24, 'Beamline': 'MEG', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})


# COBRA profile
datasets.append({'fileName' : 'Data_2022_MEG/COBRA/rasterscan.txt', 'QSK41cur' : 18.50, 'QSK42cur' : -44.1, 'QSK43cur' : 43, 'SML41cur' : -25, 'SMH41' : 200, 'SMV41' : 72.5, 'Data type - 1' : 'RasterScan', 'Data type - 2' : 'horizontal', 'Simulation n.' : 25, 'Beamline': 'MEGCOBRA', 'PILL position' : 'COBRA', 'LL' : 0, 'Chi2' : 0})
#datasets.append({'fileName' : 'Data_2022_MEG/COBRA/raster_mu_11.txt', 'QSK41cur' : 18.50, 'QSK42cur' : -44.1, 'QSK43cur' : 43, 'SML41cur' : -25, 'SMH41' : 200, 'SMV41' : 72.5, 'Data type - 1' : 'RasterScan', 'Data type - 2' : 'horizontal', 'Simulation n.' : 56, 'Beamline': 'MEGCOBRA', 'PILL position' : 'COBRA', 'LL' : 1, 'Chi2' : 1})
datasets.append({'fileName' : 'Data_2022_MEG/COBRA/raster_mu_11.txt', 'QSK41cur' : 18.50, 'QSK42cur' : -44.1, 'QSK43cur' : 43, 'SML41cur' : -10, 'SMH41' : 200, 'SMV41' : 72.5, 'Data type - 1' : 'RasterScan', 'Data type - 2' : 'horizontal', 'Simulation n.' : 56, 'Beamline': 'MEGCOBRA', 'PILL position' : 'COBRA', 'LL' : 1, 'Chi2' : 1})
 
# ------------------------------------------------------------------------------------ #
# Mu3e files

# Collimator
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_30A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 30, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 26, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_31A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 31, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 27, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_32A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 32, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 28, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_33A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 33, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 29, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_34A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 34, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 30, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_348A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 34.8, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 31, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_35A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 35, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 32, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_36A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 36, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 33, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_37A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 37, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 34, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_38A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 38, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 35, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_39A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 39, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 36, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_40A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 40, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 37, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/Collimator/QSK43_41A_180kV_fastScan.txt', 'QSK41cur' : 18.20, 'QSK42cur' : -40.70, 'QSK43cur' : 41, 'SML41cur' : -10, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 38, 'Beamline': 'Mu3e', 'PILL position' : 'Collimator', 'LL' : 0, 'Chi2' : 0})

# QSM41 
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_250.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 250, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 39, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_240.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 240, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 40, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_230.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 230, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 41, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_220.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 220, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 42, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_200.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 200, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 43, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_190.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 190, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 44, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_180.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 180, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 45, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_150.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 150, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 46, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_120.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 120, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 47, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_060.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 60, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 48, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_030.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 30, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 49, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_000.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : 0, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 50, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_-030.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : -30, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 51, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_-090.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : -90, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 52, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_-150.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : -150, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 53, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})
datasets.append({'fileName' : 'Data_2022_Mu3e/QSM41/QSM41_-250.txt', 'QSK41cur' : 11, 'QSK42cur' : -35.5, 'QSK43cur' : 30, 'SML41cur' : 0, 'ASL41cur' : -74.7, 'QSO41cur' : 56, 'QSO42cur': -23, 'ASK41cur' : -92, 'QSM41cur' : -250, 'Data type - 1' : 'QuadScan', 'Data type - 2' : '', 'Simulation n.' : 54, 'Beamline': 'Mu3eQSM', 'PILL position' : 'QSM41', 'LL' : 0, 'Chi2' : 0})

# HULK
datasets.append({'fileName' : 'Data_2022_Mu3e/HULK/scan_2022-05-20-22-31_PILL.txt', 'QSK41cur' : 4.80, 'QSK42cur' : -31.8, 'QSK43cur' : 28.80, 'SML41cur' : -14, 'ASL41cur' : -74.00, 'QSO41cur' : 53.50, 'QSO42cur': -15, 'ASK41cur' : -90.50, 'QSM41cur' : 92, 'Data type - 1' : 'RasterScan', 'Data type - 2' : '', 'Simulation n.' : 55, 'Beamline': 'Mu3eHULK', 'PILL position' : 'HULK', 'LL' : 0, 'Chi2' : 0})

# ------------------------------------------------------------------------------------ #
# Simulation settings
simulations = []
simulations = {'USbeam' : 'USbeam.root', 'USbeamName' : 'beam', 'DSbeam' : 'PepperPotPhaseSpace.root', 'DSbeamName' : 'beam', 'MEG' : 'MEGconfiguration.g4bl', 'MEGCOBRA' : 'MEGCOBRAconfiguration.g4bl', 'Mu3e' : 'Mu3econfiguration.g4bl', 'Mu3eQSM' : 'Mu3eQSMconfiguration.g4bl', 'Mu3eHULK' : 'Mu3eHULKconfiguration.g4bl'}

# Pepperpot parametrisation
pepperpot = []
pepperpot.append({'x' : -37.5, 'A' : 0.305025, 'mu' : -7.61315,  's1' : 47.6013, 'l1' : 21.3552, 's2' : 59.2614, 'l2' : 0.000606746})
pepperpot.append({'x' : -25,   'A' : 1.25203,  'mu' : 17.5435,   's1' : 71.0772, 'l1' : -13.8584, 's2' : 79.4099, 'l2' : 0.000208319})
pepperpot.append({'x' : -12.5, 'A' : 2.21984,  'mu' : -3.37802,  's1' : 74.0407, 'l1' : -10.0195, 's2' : 83.4557, 'l2' : -1.43565})
pepperpot.append({'x' :   0,   'A' : 2.27543,  'mu' : -0.708914, 's1' : 69.8991, 'l1' : 11.4565, 's2' : 84.0871, 'l2' : -9.79076})
pepperpot.append({'x' :  12.5, 'A' : 1.71837,  'mu' : -11.2332,  's1' : 77.5932, 'l1' : 4.24545, 's2' : 81.6965, 'l2' : -8.52998})
pepperpot.append({'x' :  25,   'A' : 0.842063, 'mu' : -5.04023,  's1' : 87.4775, 'l1' : -0.0166016, 's2' : 76.8209, 'l2' : 17.7025})
pepperpot.append({'x' :  37.5, 'A' : 0.276368, 'mu' : -36.5828,  's1' : 56.2147, 'l1' : 0.0178001, 's2' : 80.8401, 'l2' : 8.48725})

pepperpot.append({'y' : -37.5, 'A' : 0.167254, 'mu' : -45.9839,  's1' : 53.9635, 'l1' : -11.1519, 's2' : 67.1783, 'l2' : -0.00220219})
pepperpot.append({'y' : -25, 'A' : 0.603629, 'mu' : -29.0109,  's1' : 47.6519, 'l1' : 25.8495, 's2' : 68.406, 'l2' : -0.521432})
pepperpot.append({'y' : -12.5, 'A' : 1.28803, 'mu' : -10.2674,  's1' : 70.5986, 'l1' : -1.91722, 's2' : 62.9971, 'l2' : -2.07289})
pepperpot.append({'y' : 0, 'A' : 2.28991, 'mu' : -0.215761,  's1' : 65.043, 'l1' : -7.02367, 's2' : 55.8103, 'l2' : -11.5799})
pepperpot.append({'y' : 12.5, 'A' : 1.64781, 'mu' : -2.13186,  's1' : 64.3065, 'l1' : -2.36211, 's2' : 69.9394, 'l2' : -3.55077})
pepperpot.append({'y' : 25, 'A' : 1.22517, 'mu' : -1.38467,  's1' : 64.7991, 'l1' : 0.265646, 's2' : 59.8198, 'l2' : -14.4382})
pepperpot.append({'y' : 37.5, 'A' : 0.427013, 'mu' : 6.17808,  's1' : 47.7518, 'l1' : -10.2908, 's2' : 71.9936, 'l2' : 2.38926})

# New pepperpot parametrisation, gauss only
newPepperpot = []
newPepperpot.append({'x': -36.31264331776868, 'A': 0.5643745388196113, 'mu1': -73.34404385295751, 's1': 22.72744578394837, 'mu2': 10.800024284016454, 's2': 27.18914883345468, 'f': 0.05681969095654016})
newPepperpot.append({'x': -25.027902011569537, 'A': 3.0320637122256384, 'mu1': -16.13041569525755, 's1': 49.87962485275952, 'mu2': 23.386964154610897, 's2': 42.786478497707755, 'f': 0.22290128217176547})
newPepperpot.append({'x': -11.312643317768684, 'A': 5.563111046239338, 'mu1': 0.8717970241489227, 's1': 48.45707606338229, 'mu2': 19.038244849303325, 's2': 48.341152392144565, 'f': 0.45382446688281636})
newPepperpot.append({'x': -0.027902011569536915, 'A': 5.77282142739605, 'mu1': -16.18619657851377, 's1': 40.532343825093534, 'mu2': 12.769425709535305, 's2': 54.65238204289334, 'f': 0.4260651406032776})
newPepperpot.append({'x': 13.687356682231316, 'A': 4.374812214443779, 'mu1': -19.661271874686506, 's1': 34.62155184716665, 'mu2': 4.466625500701071, 's2': 52.41623640498592, 'f': 0.17025581748287089})
newPepperpot.append({'x': 24.972097988430463, 'A': 2.240618262595665, 'mu1': -18.400328672643823, 's1': 50.94239411502754, 'mu2': 87.34498069136859, 's2': 22.72732555532859, 'f': 0.9679379370434416})
newPepperpot.append({'x': 38.68735668223132, 'A': 0.5976944729321507, 'mu1': -41.698122506200484, 's1': 22.727289410417306, 'mu2': 12.637396866803378, 's2': 34.86589416976656, 'f': 0.5487896680842285})
newPepperpot.append({'y': -36.816758358909254, 'A': 0.3244040662809833, 'mu1': -4.595102851520112, 's1': 22.72727301600385, 'mu2': -49.784548826633674, 's2': 22.785035886526085, 'f': 0.5082145254182605})
newPepperpot.append({'y': -24.310749726243262, 'A': 1.2309380516308326, 'mu1': -9.59618209049057, 's1': 31.321105295142377, 'mu2': -26.12698494240888, 's2': 56.81776681498066, 'f': 0.7567792087231802})
newPepperpot.append({'y': -11.816758358909256, 'A': 2.678275989823482, 'mu1': -15.12176605273139, 's1': 33.85176169202702, 'mu2': 25.507914202942974, 's2': 24.342726097974893, 'f': 0.6894145007847918})
newPepperpot.append({'y': 0.6892502737567369, 'A': 4.620844156975463, 'mu1': 4.28785463280193, 's1': 39.44728996611331, 'mu2': 13.0915292114735, 's2': 24.158148267701396, 'f': 0.7626030617616371})
newPepperpot.append({'y': 13.183241641090744, 'A': 3.4735389294521957, 'mu1': 13.838500151459176, 's1': 37.73496366803156, 'mu2': -18.13612737813248, 's2': 22.72741550140353, 'f': 0.8524066828807534})
newPepperpot.append({'y': 25.689250273756738, 'A': 2.507595253928486, 'mu1': 37.764342140515865, 's1': 43.158339842084395, 'mu2': -0.16589395908461504, 's2': 32.04689100519966, 'f': 0.1944874655961128})
newPepperpot.append({'y': 38.183241641090746, 'A': 0.8306406478762063, 'mu1': 2.7287942341329923, 's1': 22.72727335706408, 'mu2': 48.162097843521316, 's2': 28.874258921801946, 'f': 0.6154068150499374})

# ------------------------------------------------------------------------------------ #
# Invert beam simulation settings
invert = {'Beamline' : 'MEGconfiguration.g4bl', 'QSK41cur' : -18.1982, 'QSK42cur' : 40.7008, 'QSK43cur' : -34.8, 'SML41cur' : 10, 'beamPositionZ' : 1250+1117-44, 'poszPILL' : 0}
simulations['Invert'] = invert
# ------------------------------------------------------------------------------------ #
# Configurations settingsi
configurations = {'datasets' : datasets, 'simulations' : simulations, 'pepperpot' : pepperpot, 'newPepperpot' : newPepperpot}

# ------------------------------------------------------------------------------------ #
with open('configurations.yaml', 'w') as f: 
	data = yaml.dump(configurations, f)

