FROM    python:3.12

WORKDIR /usr/src/app

RUN export LANG=C.UTF-8
RUN apt-get update && apt-get upgrade -y
RUN apt-get install vim iputils-ping -y

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
