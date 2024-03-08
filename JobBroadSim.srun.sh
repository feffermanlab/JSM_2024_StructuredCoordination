#!/bin/bash

#SBATCH --job-name=RunBroadSim
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --array=0-99
#SBATCH --mem-per-cpu=1G

module load Python networkx/2.8.4-foss-2022a matplotlib/3.5.2-foss-2022a
python --version

python SCBroadSim.py $SLURM_ARRAY_TASK_ID

