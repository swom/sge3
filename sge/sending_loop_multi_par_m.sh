#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --mem=500MB
#SBATCH --job-name=bt_sending_loop
#SBATCH --output=bt_sending_loop%j.log



# Declare arrays 

RUN=($(seq 0 1 30))

# Nested loops to iterate over permutations

for run in "${RUN[@]}"
do
  echo "run: $run"
  sbatch sending_trillions_m1.sh $run
  sbatch sending_trillions_m2.sh $run
done
