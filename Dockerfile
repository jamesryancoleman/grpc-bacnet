FROM python:3.13.1-slim-bookworm

RUN python -m pip install grpcio-tools
RUN python -m pip install grpcio

RUN python -m pip install bacpypes3

RUN mkdir -p /opt/bos/device/drivers/bacnet
WORKDIR /opt/bos/device/drivers/bacnet

COPY . /opt/bos/device/drivers/bacnet/

CMD ["python", "server.py"]