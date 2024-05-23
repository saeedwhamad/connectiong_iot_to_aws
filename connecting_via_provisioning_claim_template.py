from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import sys
import subprocess
import re

csr_certificate =sys.argv[1]

# Configuration
# fill this varaibles with your spesific values
client_id = ""
endpoint = ""
root_ca = ""
private_key = ""
certificate = ""
template_name = ""

# Initialize MQTT client
client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

# Configure MQTT connection parameters
client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Read the CSR
with open(csr_certificate, "r") as csr_file:
    csr_pem = csr_file.read()

# Define the payload
payload = {
    "certificateSigningRequest": csr_pem
}

# Global variables to store ownership token and certificate ID
ownership_token = None
certificate_id = None

# Function to handle the response
def custom_callback(client, userdata, message):
    global ownership_token, certificate_id
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    # Parse the JSON payload
    message_payload = json.loads(message.payload)

    # Extract ownershipToken and certificateId if the message is from the accepted topic
    if message.topic == "$aws/certificates/create-from-csr/json/accepted":
        ownership_token = message_payload.get("certificateOwnershipToken")
        certificate_id = message_payload.get("certificateId")

        # Print the extracted values
        print(f"ownershipToken: {ownership_token}")
        print(f"certificateId: {certificate_id}")

# Connect and publish
client.connect()
client.subscribe("$aws/certificates/create-from-csr/json/accepted", 1, custom_callback)
client.subscribe("$aws/certificates/create-from-csr/json/rejected", 1, custom_callback)
time.sleep(2)

# Publish the CSR
client.publish("$aws/certificates/create-from-csr/json", json.dumps(payload), 1)

# Wait for a while to receive the response
time.sleep(10)

# Disconnect
client.disconnect()


# Parameters for provisioning (if required by your template)
parameters = {
    "SerialNumber": "1234",  # Example parameter, adjust as needed
    "AWS::IoT::Certificate::Id": certificate_id
}

# Initialize MQTT client
client = AWSIoTMQTTClient(client_id)
client.configureEndpoint(endpoint, 8883)
client.configureCredentials(root_ca, private_key, certificate)

# Configure MQTT connection parameters
client.configureOfflinePublishQueueing(-1)  # Infinite offline publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

# Prepare the payload
payload = {
    "certificateOwnershipToken": ownership_token,
    "parameters": parameters
}

# Define the callback to handle responses
def custom_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Connect and publish
client.connect()
client.subscribe(f"$aws/provisioning-templates/{template_name}/provision/json/accepted", 1, custom_callback)
client.subscribe(f"$aws/provisioning-templates/{template_name}/provision/json/rejected", 1, custom_callback)
time.sleep(2)

# Publish the RegisterThing request
client.publish(f"$aws/provisioning-templates/{template_name}/provision/json", json.dumps(payload), 1)

# Wait for a while to receive the response
time.sleep(10)

# Disconnect
client.disconnect()


