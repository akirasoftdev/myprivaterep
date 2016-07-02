#!/bin/bash

/opt/local/bin/virtualenv venv -p /opt/local/bin/python2.7
. venv/bin/activate

pip install awscli
pip install --upgrade awsebcli

pushd deploy
eb create --cfg Custom-env-sc mansion-prediction-dev
popd
