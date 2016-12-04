#!/bin/bash

pushd Mansion
/opt/google-cloud-sdk/bin/dev_appserver.py --host 192.168.1.9 -A masion-prediction .
popd
