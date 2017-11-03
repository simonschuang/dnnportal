FROM ubuntu:16.04
MAINTAINER simon.s.chuang@gmail.com


ENV DNNPORT_VERSION=master
ENV DNNPORT_ROOT=/opt/dnnport

RUN apt-get update && apt-get install -y \
        git \
        liblcms2-dev \
        libfreetype6-dev \
        libjpeg8-dev \
        libtiff5-dev \
        libwebp-dev \
        python-numpy \
        python-pip \
        python-tk \
        tcl8.6-dev \
        tk8.6-dev \
        vim \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone -b ${DNNPORT_VERSION} https://github.com/simonschuang/dnnportal.git ${DNNPORT_ROOT} && \
    pip install --upgrade pip && \
    pip install -r ${DNNPORT_ROOT}/requirements.txt

WORKDIR /workspace/

CMD bash
