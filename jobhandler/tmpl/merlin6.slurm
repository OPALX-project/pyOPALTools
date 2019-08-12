#!/bin/bash -l
#SBATCH --partition=@QUEUE@
#SBATCH --nodes=@NODES@
#SBATCH --ntasks-per-core=@TASKS-PER-CORE@
#SBATCH --cpus-per-task=@CPUS-PER-TASK@
#SBATCH --ntasks-per-node=@CORES-PER-NODE@
#SBATCH --mem=@RAM-PER-NODE@
#SBATCH --time=@TIME@
#SBATCH --job-name=@SIM@
#SBATCH --error=@SIM@.error
#SBATCH --output=@SIM@.output
#SBATCH --clusters=merlin6

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

mpirun @EXEC@ @ARGS@
