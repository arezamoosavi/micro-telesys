FROM python:3.7.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PIP_FORMAT=legacy

RUN apt-get -y update && apt-get install -y python-pip python-dev libzbar-dev bash \
    gcc python3-dev git libc-dev

RUN echo 'deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main' >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apt-utils

RUN apt-get install -y netcat && apt-get autoremove -y

RUN adduser --disabled-password --gecos '' myuser

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yml ./
COPY run.sh ./
COPY services.py ./

RUN chmod +x ./run.sh

CMD ["./run.sh"]
