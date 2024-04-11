#!/bin/bash

## Begin SLURM Batch Commands

#SBATCH --job-name=snakes
#SBATCH --output=output.log
#SBATCH --cpus-per-task=2
#SBATCH --time=14-00:00
#SBATCH --mail-type=BEGIN,END,FAIL         # Email events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=melosydrose@gmail.com  # Your email address

module load python3
python main.py ./data/Snakes.txt Snakes 4


## ** End Of SLURM Batch Commands **
##
## ===================================
## Important Hickory GPU Request Note
## ===================================
## Most importantly, the option `--gres=gpu:<type>:<count>` must be used
## to request GPUs (`-G` or `--gpus` will not work). Values for `<type>`
## are `40g` and `80g`, referring to the 40 GB and 80 GB GPUs. The current
## limits (`<count>`) for the 40 GB GPUs are 1 in the `long` QOS and 2 in
## `short`. The current limit for the 80 GB GPUs is 1 in `short` (they are
## unavailable in `long`).
##
##
## More Info: https://wiki.vcu.edu/x/P6POBQ
##
## END