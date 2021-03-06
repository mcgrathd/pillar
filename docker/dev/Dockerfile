FROM ubuntu
MAINTAINER Francesco Siddi <francesco@blender.org>

RUN apt-get update && apt-get install -y \
python \
python-dev \
python-pip \
git \
nano \
zlib1g-dev \
libjpeg-dev \
python-crypto \
python-openssl \
libssl-dev \
libffi-dev \
software-properties-common

RUN add-apt-repository ppa:mc3man/trusty-media \
&& apt-get update && apt-get install -y \
ffmpeg


RUN mkdir /data \
&& mkdir /data/www \
&& mkdir /data/www/pillar \
&& mkdir /data/dev \
&& mkdir /data/dev/pillar \
&& mkdir /storage \
&& mkdir /storage/shared \
&& mkdir /storage/pillar \
&& mkdir /data/config \
&& mkdir /storage/logs

RUN git clone https://github.com/armadillica/pillar.git /data/www/pillar

RUN pip install virtualenv \
&& virtualenv /data/venv
RUN . /data/venv/bin/activate && pip install -r /data/www/pillar/requirements.txt

VOLUME /data/dev/pillar
VOLUME /data/config
VOLUME /storage/shared
VOLUME /storage/pillar

ENV MONGO_HOST mongo_pillar

EXPOSE 5000

ADD runserver.sh /runserver.sh

ENTRYPOINT ["bash", "/runserver.sh"]
