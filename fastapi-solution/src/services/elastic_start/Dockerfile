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

CMD ["python3.10", "etl_start.py"]