#for RECORDING!!! Finally!
from mss import MSS
from PIL import Image
from io import BytesIO
import time

#lookout api
import httpx2
from datetime import datetime, timezone

# config stuff
from pathlib import Path
import json
import os
import psutil

#temp
import sys

#frame stuff
framesCaptured = 0

#config
userToken = "AhhhAlmostAlmost"
pidPath = Path(__file__).resolve().parent.parent / "temp" / "recorderPID"
configPath = Path(__file__).resolve().parent.parent / "config" / "userConfig.json"

#api
lapse_api_url = "https://api.lapse.hackclub.com/api"
lookout_api_url = "https://lookout.hackclub.com/api"

def takeScreenshot(sct, token):

    # get upload url
    isodate = datetime.now().astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    print(isodate)
    response = httpx2.get(
        url=lookout_api_url + f"/sessions/{token}/upload-url?capturedAt={isodate}"
    ).json()
    print(response)

    #send image to retrieved upload url
    monitor = sct.monitors[1]
    screenshot = sct.grab(monitor)
    image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    buffer = BytesIO()
    image.save(buffer, format="JPEG", optimize=True)
    response2 = httpx2.put(
        url=response["uploadUrl"],
        content=buffer.getvalue(),
        headers={"Content-Type": "image/jpeg"},
    )
    print(response2.is_error)

    width, height = screenshot.size
    #send confirmation to lookout we sent image
    response3 = httpx2.post(
        url= lookout_api_url + f"/sessions/{token}/screenshots",
        json={
            "screenshotId":response["screenshotId"],
            "width":width,
            "height":height,
            "fileSize": len(buffer.getvalue())
        }
    ).json()
    time.sleep(
        datetime.fromisoformat(response3["nextExpectedAt"]).timestamp() - datetime.now().timestamp()
    )

# loop that actually records video
def beginRecording():
    # create a lookout recording
    lookoutSession = None
    response = httpx2.post(
        url= lapse_api_url + "/timelapse/createRecordingSession",
        headers= { 
            "Authorization": "Bearer " + userToken
        },
        json={
            "mode":"screen"
        }
    )
    if (response.is_error):
        print("Error occured while starting recording. Maybe token is outdated?")
        return

    print(response.json())
    lookoutSession = response.json()["data"]
    lookout_api_url = lookoutSession["lookoutApiBaseUrl"] + "/api"

    response = httpx2.get(
        url=lookout_api_url + "/sessions/" + lookoutSession["lookoutToken"]
    )

    print(response.json())
    # write recorder path
    pidPath = Path(__file__).resolve().parent.parent / "temp" / "recorderPID"
    with open(pidPath, "w") as file:
        file.write(str(os.getpid()))

    try:
        with MSS() as sct:
            while True:
                takeScreenshot(sct, lookoutSession["lookoutToken"])
    except KeyboardInterrupt:
        print("Oop.")
    finally:
        #writer.close()
        pass



def initialize():
    global userToken
    try:
        config = None
        with open (configPath, "r") as data:
            config = json.load(data)
        userToken = config["userToken"]
    except Exception as e:
        print(e)
        print("Recording config doesn't exist or is corrupted. Using defaults.")

if __name__ == "__main__":
    with open(pidPath, "r") as file:
        if psutil.pid_exists(int(file.readlines()[0])):
            print("cannot start two recordings at once, try again after running 'timelapse stop'")
            sys.exit()
    initialize()
    beginRecording()