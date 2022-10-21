# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:16:34 2017

@author: schwendimann_p
"""

offset = 0
nRuns = 3500

jobs = open("joblist.txt", "w")

commands = "python3 /data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/optuna/optuna_LL.py\n"

for i in range(nRuns):
	run = i+offset
	slurm_file = open("/data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/slurm/trial%07i.sl" %run,"w")
	jobs.write("sbatch /data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/slurm/trial%07i.sl\n" %run)

	slurm_file.write("#!/bin/bash\n")
	slurm_file.write("#SBATCH --cluster=merlin6 \n")
	slurm_file.write("#SBATCH --partition=hourly \n")
	slurm_file.write("#SBATCH -o /data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/OUT/trial%07i.out \n" %run)
	slurm_file.write("#SBATCH -e /data/project/general/muonGroup/simulations/giovanni/PepperPotCheck/OUT/trial%07i.err \n" %run)
	slurm_file.write("#SBATCH --time 0-00:55:00\n\n")
	slurm_file.write("ulimit -c 0\n")
	slurm_file.write("echo Running on: `hostname` \n")
	slurm_file.write("TIMESTART=`date`\n")
	slurm_file.write("echo Start Time: ${TIMESTART}\n")
	slurm_file.write("echo ###################################################################\n")
	slurm_file.write("echo #     Running Environement#\n")
	slurm_file.write("echo ###################################################################\n")
	slurm_file.write("env|sort\n")
	slurm_file.write("echo ###################################################################\n")
	slurm_file.write("echo # End of Running Environement     #\n")
	slurm_file.write("echo ###################################################################\n")
	slurm_file.write(commands)
	slurm_file.write("echo Exit status: $?\n")
	slurm_file.write("echo Start Time: ${TIMESTART}\n")
	slurm_file.write("echo Stop Time: `date`\n")
	slurm_file.close()


jobs.close()
