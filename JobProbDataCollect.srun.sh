#!/bin/bash

#SBATCH --job-name=RunDataCollect
#SBATCH --output=logs/%x_%j.out
#SBATCH --mem-per-cpu=1G

module load Python networkx/2.8.4-foss-2022a matplotlib/3.5.2-foss-2022a
python --version

python ProbDataCollect.py 

