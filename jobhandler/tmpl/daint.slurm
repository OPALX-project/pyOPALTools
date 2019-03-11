#!/bin/bash -l


#SBATCH --partition=_QUEUE_
#SBATCH --nodes=_NODES_
#SBATCH --ntasks-per-core=_TASKS-PER-CORE_
#SBATCH --cpus-per-task=_OPENMP_
#SBATCH --ntasks-per-node=_CORES-PER-NODE_
#SBATCH --mem=_RAM-PER-NODE_
#SBATCH --time=_TIME_
#SBATCH --job-name=_SIM_
#SBATCH --error=_SIM_.error
#SBATCH --output=_SIM_.output
#SBATCH --constraint=mc
#SBATCH --account=_ACCOUNT_

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load daint-mc

srun _EXEC_ _ARGS_
