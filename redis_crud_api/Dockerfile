FROM python:3.12.4-bookworm

RUN apt-get update -y && apt-get upgrade -y \
    && pip3 install fastapi redis redis-client pydantic typing pytest

WORKDIR /app
COPY ./main.py /app
COPY ./models.py /app


EXPOSE 8004

ENTRYPOINT [ "fastapi", "run", "main.py", "--port", "8004"]