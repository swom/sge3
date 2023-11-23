#!/bin/bash
#SBATCH --time=12:10:00
#SBATCH --mem=2GB
#SBATCH --job-name=sge_job_static
#SBATCH --output=logs/sge_job_static%j.log


export PATH=$HOME/.local/bin:$PATH
module load Python
pip install numpy
pip install PyYAML
pip install tqdm

echo "sge_job_static ==> dev: $1, meta: $2, start_mut_rate: $4, run: $3, crossover_rate: $5"

python -m examples.symreg --experiment_name /scratch/p288427/megalomania/sge_static --grammar grammars/regression_pagie.pybnf --parameters parameters/standard_static.yml --run $1 --seed $1 
