#!/bin/bash
Sudo apt update
sudo apt install cmake
sudo apt install openssl
sudo apt install libssl-dev

git clone https://github.com/awslabs/aws-iot-device-client
cd aws-iot-device-client
mkdir build
cd build
cmake ../
cmake ––build . ––target aws-iot-device-client
# Setup
cd ../
./setup.sh # At this point you’ll need to respond to prompts for information, including paths to your thing certs (“when ask for public key you have to put example.cert.pem”)

# Run the AWS IoT Device Client
./aws-iot-device-client # This command runs the executable
