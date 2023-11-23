#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --mem=500MB
#SBATCH --job-name=bt_sending_loop
#SBATCH --output=bt_sending_loop%j.log



# Declare arrays 
DEV=("0.1" "0.01" "0.001") 
META=("1.0" "0.1") 
MUT_R=("0.1" "0.01")
CR_R=("0.9" "0.01")
RUN=($(seq 0 1 30))

# Nested loops to iterate over permutations
for dev in "${DEV[@]}"
do
  for meta in "${META[@]}"
  do
    for cr in "${CR_R[@]}"
    do 
      for mut in "${MUT_R[@]}"
      do 
        for run in "${RUN[@]}"
        do
          echo "dev: $dev, meta: $meta, start_mut_rate: $mut, run: $run, crossover_rate: $cr"
          sbatch sending_trillions.sh $dev $meta $run $mut $cr
        done
      done
    done
  done
done
