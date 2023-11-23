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

echo "dev: $1, meta: $2, start_mut_rate: $4, run: $3, crossover_rate: $5"

python -m examples.symreg --experiment_name /scratch/p288427/megalomania/sge_m2 --run $3 --seed $3 --parameters parameters/m_parameters2.yml --grammar grammars/regression_pagie.pybnf --gauss_sd $1 --prob_mutation_probs $2  --prob_mutation $4 --prob_crossover $5
