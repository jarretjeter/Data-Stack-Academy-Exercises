FROM python:3.7.10-slim-buster

WORKDIR /home

COPY data/potato_salad.yml main.py requirements.txt ./

RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]