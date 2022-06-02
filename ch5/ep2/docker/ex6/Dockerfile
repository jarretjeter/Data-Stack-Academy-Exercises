FROM python:3.7.10-slim-buster

# adding env variables
ENV INPUT_FILE="/home/deb-airports.csv" \
    NUM_ROWS=10

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install -r requirements.txt

# create a volume and initialize the history sqlite3 database
RUN mkdir /data
# initialize the sqlite database by calling version once
RUN python main.py -d /data/history.db version
# add the volume
VOLUME [ "/data" ]

# add an ENTRYPOINT
ENTRYPOINT ["python", "main.py", "-d", "/data/history.db"]
CMD ["print"]
