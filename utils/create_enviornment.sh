#!/usr/bin/env bash

# confirm your server have install `anaconda`
# (NOTE: in this phase, you need confirm the installation via enter `Y` manually)
conda create -n pranet python=3.6

# activate your virtual environment
# (NOTE: if this step is invalid, you must activate it manually)
conda activate pranet

# install necessary packages for PyTorch
# (NOTE: in this phase, you need confirm the installation via enter `Y` manually)
conda install pytorch=1.3.1 torchvision=0.4.2 cudatoolkit=10.0

# install necessary packages for necessary libs
pip install opencv-python==3.4.2.17 tensorboardX==2.0

# run the inference script
python Testing.py