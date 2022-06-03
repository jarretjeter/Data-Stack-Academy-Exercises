FROM python:3.7.10-slim-buster

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# set the working directory
WORKDIR /home

# add source files to the image
COPY main.py .
COPY requirements.txt .

# install pip requirements
RUN pip3 install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 4 threads.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 main:app
