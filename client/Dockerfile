FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY client.py wait_for_server.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python3 wait_for_server.py && python3 client.py"]