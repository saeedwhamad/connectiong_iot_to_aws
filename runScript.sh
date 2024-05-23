#!/bin/bash
pip install AWSIoTPythonSDK
openssl genpkey -algorithm RSA -out device_private.key
openssl req -new -key device_private.key -out device.csr
python3 code.py "/device.csr"
