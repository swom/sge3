#!/bin/bash
#SBATCH --time=12:10:00
#SBATCH --mem=500MB
#SBATCH --job-name=sge_job
#SBATCH --output=logs/sge_job%j.log


export PATH=$HOME/.local/bin:$PATH
module load Python
pip install numpy
pip install PyYAML
pip install tqdm

python -m examples.symreg --experiment_name /scratch/p288427/megalomania/sge --run $3 --seed $3 --parameters parameters/standard.yml --grammar grammars/regression_pagie.pybnf --gauss_sd $1 --prob_mutation_probs $2  --prob_mutation $4
