import tusclient

# for config
from pathlib import Path
import json

configPath = Path(__file__).resolve().parent.parent / "config" / "userConfig.json"
userToken = "COMOSEDICELICKMYSTICK"

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