#!/bin/bash -l

#SBATCH --job-name=_SIM_
#SBATCH --error=_SIM_.error
#SBATCH --output=_SIM_.output
#SBATCH --partition=merlin
#SBATCH --time=_TIME_
#SBATCH --nodes=_NODES_
#SBATCH --ntasks=_CORES_
#SBATCH --ntasks-per-node=_CORES-PER-NODE_
#SBATCH --mem=_RAM-PER_NODE_

mpirun _EXEC_ _ARGS_
