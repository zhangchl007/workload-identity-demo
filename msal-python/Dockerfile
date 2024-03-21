FROM python:3.9.18-alpine
COPY requirements.txt /requirements.txt
COPY . /app
WORKDIR /app
RUN apk update &&  \
    apk add --no-cache --update wget iperf3 && \
    pip3 install -r /requirements.txt
# Kubernetes runAsNonRoot requires USER to be numeric
USER 1001
#CMD ["iperf3", "-s"]
CMD ["python","main.py"]
