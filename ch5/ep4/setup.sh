#/bin/bash

# this script will setup the environment and install all necessary components 
# of Data Stack Academy (DSA) Chapter 5 Episode 4

# install/upgrade virtualenv
python3.7 -m pip install --upgrade virtualenv

# create and run a python3.7 virtual env
python3.7 -m venv ch5e4_venv
source ch5e4_venv/bin/activate
# install/upgrade pip
python3.7 -m pip install --upgrade pip setuptools wheel
# pip install pypi packages
pip install -r requirements.txt
# change default theme and fonts
jt -t onedork -T -tf sourcesans -nf sourcesans -tfs 12
