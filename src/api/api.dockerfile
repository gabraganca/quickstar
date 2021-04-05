FROM python:3.9.3-alpine
LABEL maintainer="ga.braganca@gmail.com"

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && pip install --no-cache-dir uvicorn \
    && apk del .build-deps gcc libc-dev make

RUN addgroup -S api && adduser -S api -G api
WORKDIR /home/api/
RUN chown api:api /home/api
USER api
ENV PATH="/home/api/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
COPY . .