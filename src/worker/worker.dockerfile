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

ENV SYNSPEC_DIRPATH /home/worker/app/synspec