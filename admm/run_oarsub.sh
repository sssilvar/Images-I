#!/usr/bin/env bash

#oarsub -I -p "gpu='YES' and gpucapability >= '5.0'" -l /gpunum=1,walltime=3:00:00
#source ~/Softwares/virt_tf/bin/activate
#module load cuda/9.1
#module load cudnn/7.0-cuda-9.1
#module load tensorflow/1.6-python3-cuda9.1

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

module load cuda/8.0
CMD="python "${CURRENT_DIR}"/admm_pytorch.py"