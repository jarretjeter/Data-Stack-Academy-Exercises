FROM python:3.7.10-slim-buster

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install -r requirements.txt

# add an ENTRYPOINT
# ENTRYPOINT specifies the script to run for every docker run
# CMD here provides default args to the ENTRYPOINT command
# CMD args is ignored if user specifies their own args
ENTRYPOINT ["python", "main.py"]
CMD ["print", "-n", "10"]
