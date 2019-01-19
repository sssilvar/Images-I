#!/bin/env python
import os
import configparser
from os.path import join, dirname, realpath

# Set the root folder
current_dir = dirname(realpath(__file__))

# Set config file path
cfg = join(current_dir, 'config.cfg')

# Parse configuration
config = configparser.ConfigParser()
config.read(cfg)
os.system('clear')
print(config)
print(config.get('dirs', 'code'))
print(config.get('dirs', 'home'))