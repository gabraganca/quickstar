FROM alpine as data-getter

RUN apk update && apk add --no-cache wget tar gzip

WORKDIR /home

RUN mkdir -p bstar2006 \
    && wget -c http://tlusty.oca.eu/Tlusty2002/database/BGmodels_v2.tar \
    && tar -xf  BGmodels_v2.tar -C bstar2006/ \
    && gunzip bstar2006/* \
    && rm BGmodels_v2.tar

RUN wget -c http://tlusty.oca.eu/Tlusty2002/database/atom_BS06.tar \
    && tar -xf atom_BS06.tar \
    && mv data atdata \
    && gunzip atdata/* \
    && rm atom_BS06.tar


FROM python:3.8-slim-buster as compiler

WORKDIR /synspec/

RUN apt-get update \
    && apt-get install -y --no-install-recommends gfortran \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY app/synspec .

RUN gfortran -g -fno-automatic -static -o synspec49 synspec49.f \
    && gfortran -g -fno-automatic -static -o rotin3 rotin3.f


FROM python:3.8-slim-buster
LABEL maintainer="ga.braganca@gmail.com"

ENV SHELL /bin/bash

RUN apt-get update \
    && apt-get install -y --no-install-recommends gnudatalanguage \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r worker && useradd -r -g worker worker

WORKDIR /home/worker/
RUN chown worker:worker /home/worker
USER worker
ENV PATH="/home/worker/.local/bin:${PATH}"
ENV PYTHONPATH /home/worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=worker:worker . .

COPY --from=compiler /synspec/synspec49 /home/worker/app/synspec/
COPY --from=compiler /synspec/rotin3 /home/worker/app/synspec/
COPY --from=data-getter /home/bstar2006 /home/worker/app/bstar2006/
COPY --from=data-getter /home/atdata /home/worker/app/atdata/

ENV SYNSPEC_DIRPATH /home/worker/app/synspec