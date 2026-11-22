# server stuff
import tusclient
import httpx2

# for config
from pathlib import Path
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

configPath = Path(__file__).resolve().parent.parent / "config" / "userConfig.json"
userToken = "COMOSEDICELICKMYSTICK"

def createNewAESKey():
    return AESGCM.generate_key(128)

def beginUpload(api_url):
    #alert api we're making a new draft
    response = httpx2.post(
        url= api_url + "/draftTimelapse/create",
        headers= {
            "Authorization": "Bearer " + userToken,
            "Content-Type": "application/json"
            },
        json={
            "snapshots":[],
            
        }
    )
    print(response.text)

def initialize():
    try:
        global userToken
        config = None
        with open(configPath, "r") as file:
            config = json.load(file)
        userToken = config["userToken"]
        print(userToken)
    except Exception as e:
        print(e)
        print("userConfig.json is malformed or destroyed. Uploading cannot occur.")
     

if __name__ == "__main__":
    initialize()