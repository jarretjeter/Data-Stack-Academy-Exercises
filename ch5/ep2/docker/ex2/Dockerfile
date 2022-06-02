# Dockerfile introduction
#
# Objectives:
#   - Add data files and python scripts
#   - Use RUN command to install pip requirements

# base form python3.7 image
FROM python:3.7.10-slim-buster


# set the working directory
WORKDIR /home

# add source files to the image
# pay attention how we use a wildcard to copy all files
# files that match the .dockerignore file are ignored
COPY * ./

# RUN command is used to run shell commands inside the container
# these commands can install and configure various softrware. 
# in this example we use to pip install packages
# install pip requirements
RUN pip3 install -r requirements.txt

# run the script 
CMD ["python", "main.py"]
