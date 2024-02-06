FROM python:3-alpine3.11
WORKDIR /rabbit_app
COPY . /rabbit_app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./main.py