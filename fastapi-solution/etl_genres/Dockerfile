FROM python:3.10

WORKDIR /opt/etl_genres

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["python3", "main.py"]