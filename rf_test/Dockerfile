FROM python:3.8-alpine

RUN apk update && apk add curl

WORKDIR /usr/src/app

COPY tests.sh test-server.robot requirements.txt ./

RUN pip install -r requirements.txt

CMD ["sh", "tests.sh"]