#!/usr/bin/env bash
podman run -it --rm -v ~/.aws/:/root/.aws:ro nhb poetry run python neohowiebot/main.py