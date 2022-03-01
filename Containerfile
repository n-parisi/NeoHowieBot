FROM python:3.8

# System deps:
RUN pip3 install poetry
RUN apt update
RUN apt upgrade -y
RUN apt install libffi-dev -y
RUN apt install ffmpeg -y
# RUN apt install python3.8-dev

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# We need a copy of pycord until 2.0 is released
COPY dep/ dep/

# Copy source code
COPY neohowiebot/ /code/neohowiebot

# Copy secrets
COPY secrets.env /code

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi