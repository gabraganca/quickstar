FROM python:3.8-slim-buster
LABEL maintainer="ga.braganca@gmail.com"

RUN groupadd -r frontend && useradd -r -g frontend frontend
WORKDIR /home/frontend/
RUN chown frontend:frontend /home/frontend
USER frontend
ENV PATH="/home/frontend/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN echo $PWD > ~/.local/lib/python3.8/site-packages/app.pth

COPY . .