#!/bin/bash


#/ #SBATCH --job-name=gamjet_analysis         # Job name
#/ #SBATCH -p long
#/ #SBATCH --time=2-00:00:00                     # Time limit hrs:min:sec
#/ #SBATCH --account=t3
#/ #SBATCH --ntasks=1                          # Run a single task
#/ #SBATCH --cpus-per-task=1                   # Number of CPU cores per task; Example of  submitting  8-core parallel SMP job
#/ #SBATCH --mem=10gb                           # Job memory request
#/ #SBATCH --output=logs/$2/gamjet_analysis_$1_$2_%j.log                 # Standard output and error log



# python runIOVs.py -i all -v new_tot_23_pnetreg
time root -l -b -q "mk_GamHistosFill.C(\"$1\", \"$2\")"

#/ #SBATCH -w t3wn58                           # choose particular Compute Node from wn partition
#/ #SBATCH --mem-per-cpu=3072                 # example of memory request for one CPU core