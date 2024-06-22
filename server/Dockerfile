FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY server.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "server.py"]
