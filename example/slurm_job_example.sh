#!/bin/bash

#SBATCH --job-name simple-example
#SBATCH --time 00:05:00
#SBATCH --partition=<partition_name>
#SBATCH --account=<account_name>
#SBATCH --mem=50M
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --chdir=<pipeline_absolute_path>
#SBATCH --error=<pipeline_absolute_path>/slurm-%j.%N.err
#SBATCH --output=<pipeline_absolute_path>/slurm-%j.%N.out


source activate
pipeline reset ./example/
pipeline execute ./example/
pipeline await ./example/