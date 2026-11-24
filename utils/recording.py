#for RECORDING!!! Finally!
from mss import MSS
from PIL import Image
from io import BytesIO
import time

#lookout api
import httpx2
from datetime import datetime, timezone

# idk what to call this, its for the subprocess open thing
import sys
import subprocess

# config stuff
from pathlib import Path
import json
import os
import psutil



#frame stuff
framesCaptured = 0

#config
userToken = "AhhhAlmostAlmost"
pidPath = Path(__file__).resolve().parent.parent / "temp" / "recorderPID"
configPath = Path(__file__).resolve().parent.parent / "config" / "userConfig.json"
lookoutSessionPath = Path(__file__).resolve().parent.parent / "temp" / "lookoutSession.json"

#api
lapse_api_url = "https://api.lapse.hackclub.com/api"
lookout_api_url = "https://lookout.hackclub.com/api"

def takeScreenshot(sct, token):

    # get upload url
    global lookout_api_url
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
def beginRecording(isResuming):
    #if this is a resume from pausing, we don't need to create a new session
    global lookout_api_url
    lookoutSession = None
    if (not isResuming):
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
    else:
        #just grab the token from original session
        with open(lookoutSessionPath, "r") as file:
            jsonified = json.load(file)

        lookoutSession = {
            "lookoutToken": jsonified["sessionId"],
        }
    response = httpx2.get(
        url=lookout_api_url + "/sessions/" + lookoutSession["lookoutToken"]
    )
    print(response.json())

    # write recorder path
    with open(pidPath, "w") as file:
        file.write(str(os.getpid()))

    # write lookoutSession path
    with open(lookoutSessionPath, "r") as file:
        jsonified = json.load(file)
    jsonified["sessionId"] = lookoutSession["lookoutToken"]
    with open(lookoutSessionPath, "w") as file:
        file.write(json.dumps(jsonified))

    #run loop
    try:
        with MSS() as sct:
            while True:
                takeScreenshot(sct, lookoutSession["lookoutToken"])
    except KeyboardInterrupt:
        print("Oop.")
    finally:
        print("What!")
        pass

def stopRecording():
    #get sessionToken
    with open(lookoutSessionPath, "r") as file:
        jsonified = json.load(file)
    sessionToken = jsonified["sessionId"]
    jsonified["sessionId"] = ""

    #kill recording on lookout's servers and have them do the whole processing
    httpx2.post(
        url=lookout_api_url + f"/sessions/{sessionToken}/stop"
    )
    with open(lookoutSessionPath, "w") as file:
        file.write(json.dumps(jsonified))
    print("recording finished! you can see the draft in lapse.hackclub.com")

def pauseRecording():
    #get sessionToken
    with open(lookoutSessionPath, "r") as file:
        jsonified = json.load(file)
    sessionToken = jsonified["sessionId"]

    #stop Lookout and kill the original recording process
    global lookout_api_url
    httpx2.post(
        url=lookout_api_url + f"/sessions/{sessionToken}/pause"
    )
    with open(pidPath, "r") as file:
        psutil.Process(int(file.readline())).terminate()

def resumeRecording():
    #get sessionToken
    with open(lookoutSessionPath, "r") as file:
        jsonified = json.load(file)
    sessionToken = jsonified["sessionId"]
    if sessionToken == "":
        print("no recording to resume, please use 'timelapse record'!")
        return
    #restart lookout, then call beginRecording
    global lookout_api_url
    httpx2.post(
        url=lookout_api_url + f"/sessions/{sessionToken}/resume"
    )
    subprocess.Popen(
        [sys.executable, "-m", "utils.recording"],
        start_new_session=True
    )
    
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
    with open(lookoutSessionPath, "r") as file:
        jsonified = json.load(file)
    if (jsonified["sessionId"] != ""):
        print("previous session detected! restarting lookout from that session id.")
        beginRecording(True) 
    else:
        print("beginning recording!")
        initialize()
        beginRecording(False)