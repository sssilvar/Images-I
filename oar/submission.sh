#!/bin/bash

# Submission script for the helloWorld program
#
# Comments starting with #OAR are used by the resource manager if using "oarsub -S"
#
# The job reserves 8 nodes with one processor (core) per node,
# only on xeon nodes, job duration is less than 10min
#OAR -l /nodes=1/core=5,walltime=00:10:00
#OAR -p cputype='xeon'
#
# The job is submitted to the default queue
#OAR -q default
# 
# Path to the binary to run

python3 hello_world_mc.py
