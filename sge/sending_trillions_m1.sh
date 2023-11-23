#!/bin/bash
#SBATCH --time=12:10:00
#SBATCH --mem=2GB
#SBATCH --job-name=sge_job
#SBATCH --output=logs/sge_job%j.log


export PATH=$HOME/.local/bin:$PATH
module load Python
pip install numpy
pip install PyYAML
pip install tqdm

echo "run: $1"

python -m examples.symreg --experiment_name /scratch/p288427/megalomania/sge_m1 --run $1 --seed $1 --parameters parameters/m_parameters1.yml --grammar grammars/regression_pagie.pybnf
