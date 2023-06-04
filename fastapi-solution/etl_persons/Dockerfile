FROM python:3.10

WORKDIR /opt/etl

RUN groupadd -r web && useradd -d /opt/etl -r -g web web \
    && chown web:web -R /opt/etl

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown web:web -R .

RUN chmod +x run.sh

USER web

ENTRYPOINT ["/opt/etl/run.sh"]