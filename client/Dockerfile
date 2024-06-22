FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY client.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python3", "client.py"]
