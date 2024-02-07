FROM python:3-alpine3.12
WORKDIR /rabbit_app
COPY . /rabbit_app
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./maincopy.py