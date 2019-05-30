FROM python:3.7-slim-stretch

COPY . /graph-flow
WORKDIR /graph-flow

RUN pip3 install ../graph-flow

ENTRYPOINT ["python3", "-m", "graphflow"]
