FROM python:3.12.4-bookworm

RUN apt-get update -y && apt-get upgrade -y \
    && pip3 install fastapi requests
WORKDIR /app
COPY ./main.py /app

EXPOSE 8000

ENTRYPOINT [ "fastapi", "run", "main.py", "--port", "8000"]