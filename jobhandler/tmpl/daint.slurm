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
#SBATCH --constraint=mc
#SBATCH --account=@ACCOUNT@

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load daint-mc

srun @EXEC@ @ARGS@
