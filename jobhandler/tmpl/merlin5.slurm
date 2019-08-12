#!/bin/bash -l
#SBATCH --job-name=@SIM@
#SBATCH --error=@SIM@.error
#SBATCH --output=@SIM@.output
#SBATCH --partition=merlin
#SBATCH --time=@TIME@
#SBATCH --nodes=@NODES@
#SBATCH --ntasks=@CORES@
#SBATCH --ntasks-per-node=@CORES-PER-NODE@
#SBATCH --mem=@RAM-PER-NODE@

mpirun @EXEC@ @ARGS@
