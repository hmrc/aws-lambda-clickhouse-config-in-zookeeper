#!/bin/bash

set -xeou
yum install -y zip amazon-linux-extras
amazon-linux-extras enable python3.8
yum install -y python3.8 python3-pip
python3.8 -V
pip3 -V

BASE_DIR=/data
PIP_PACKAGES_DIR=${BASE_DIR}/lambda-packages

cd ${BASE_DIR}

zip clickhouse_config_in_zookeeper.zip clickhouse_config_in_zookeeper.py

mkdir -p ${PIP_PACKAGES_DIR}
pip3 install --upgrade pip
pip3 install -t ${PIP_PACKAGES_DIR} -r requirements.txt
cd ${PIP_PACKAGES_DIR}
zip -r ../clickhouse_config_in_zookeeper.zip .
