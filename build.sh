#!/bin/bash

rm -rf build/
mkdir build

cp bins.py build
cp handler.py build
cd build
zip build.zip bins.py handler.py


echo "Update the code with:"
echo "aws lambda update-function-code get-function-configuration  --function-name bincollection-prod-skill --region eu-west-1"
