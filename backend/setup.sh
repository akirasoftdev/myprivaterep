#!/bin/bash

DEST_DIR=deploy

rm -rf $DEST_DIR
mkdir -p $DEST_DIR

cp requirements.txt $DEST_DIR
if [ -f deploy/tensorflow-0.12.0rc0-cp27-none-linux_x86_64.whl ]; then
	echo "already downloaded"
else
	wget -P $DEST_DIR https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.12.0rc0-cp27-none-linux_x86_64.whl
fi
cp consts.py              $DEST_DIR/
cp -rf .elasticbeanstalk  $DEST_DIR/
cp -rf ../common          $DEST_DIR/
cp -rf ../map/data32_16   $DEST_DIR/
cp ../map/__init__.py     $DEST_DIR/
cp ../map/howmuch.py      $DEST_DIR/application.py
cp ../map/error_rate.py   $DEST_DIR/
cp ../map/nn_mansion.py   $DEST_DIR/
cp ../map/rosenka.py      $DEST_DIR/
cp ../map/utils.py        $DEST_DIR/
