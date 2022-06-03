FROM python:3.7.10-slim-buster

WORKDIR /home

RUN mkdir data

COPY main.py requirements.txt ./

COPY  data/potato_salad.yml ./data

#bash commands
RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]