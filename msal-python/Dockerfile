FROM mcr.microsoft.com/mirror/docker/library/debian:bookworm-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM python:3.9.18-alpine
COPY --from=build-venv /venv /venv
COPY requirements.txt /requirements.txt
COPY . /app
WORKDIR /app
RUN pip3 install -r /requirements.txt && apk update && apk add --no-cache --update wget iperf3
# Kubernetes runAsNonRoot requires USER to be numeric
USER 65532:65532
#CMD ["iperf3", "-s"]
CMD ["python","main.py"]
