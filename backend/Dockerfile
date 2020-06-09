FROM python:latest

WORKDIR /backend
COPY . ./backend

RUN pip3 install flask flask-cors bigchaindb_driver --upgrade setuptools bigchaindb_driver

EXPOSE 5000