FROM python:3.8

# System deps:
RUN pip3 install poetry
RUN apt update
RUN apt upgrade -y
RUN apt install libffi-dev -y
RUN apt install ffmpeg -y
# RUN apt install python3.8-dev

# Copy requirements
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Copy source code
COPY neohowiebot/ /code/neohowiebot

# Copy secrets
COPY secrets.env /code

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Start bot
CMD poetry run python neohowiebot/main.py