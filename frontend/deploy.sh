#!/bin/bash

VERSION=`date +%s`

pushd frontend

/opt/local/bin/virtualenv venv -p /opt/local/bin/python2.7
. venv/bin/activate

/opt/google-cloud-sdk/bin/gcloud auth activate-service-account mansion-prediction@appspot.gserviceaccount.com --key-file /var/lib/jenkins/gae/mansion-prediction-9e46ca921406.json
/opt/google-cloud-sdk/bin/gcloud config set account mansion-prediction@appspot.gserviceaccount.com

/opt/google-cloud-sdk/bin/gcloud app deploy Manshion/app.yaml -q -v $VERSION

popd
