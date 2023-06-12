FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get clean

RUN  pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker -b 0.0.0.0:8000 main:app