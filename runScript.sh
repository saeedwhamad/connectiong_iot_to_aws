#!/bin/bash
pip install AWSIoTPythonSDK
openssl genpkey -algorithm RSA -out device_private3.key
openssl req -new -key device_private3.key -out device.csr
python3 code.py "/device.csr"