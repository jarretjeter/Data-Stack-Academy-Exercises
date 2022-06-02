FROM python:3.7.10-slim-buster

# adding env variables with default values
ENV INPUT_FILE="/home/deb-airports.csv" \
    NUM_ROWS=10

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install -r requirements.txt

# add an ENTRYPOINT
ENTRYPOINT ["python", "main.py"]
CMD ["print"]
