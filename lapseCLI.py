import argparse
import psutil

from pathlib import Path


import subprocess
import sys

import utils.authentication 
import utils.recording
import utils.upload


# Variables
api_url = "https://api.lapse.hackclub.com/api"
actual_url = "https://lapse.hackclub.com/api"
auth_url = "https://hackatime.hackclub.com"
port = 8081

parser = argparse.ArgumentParser(description="Interact with Lapse without Lookout.")

# TODO: add arguments
parser.add_argument("option", type=str, help="")
parser.add_argument("secondaryAction", type=str)

args = parser.parse_args()

def main():
    print(args)
    if (args.option == "config"):
        if (args.secondaryAction == "token"):
            utils.authentication.getAuthToken(api_url, port)
        elif (args.secondaryAction == "register"):
            utils.authentication.registerDevice(api_url)
            pass
    elif (args.option == "timelapse"):
        if (args.secondaryAction == "record"):
            subprocess.Popen(
                [sys.executable, "-m", "utils.recording"],
                start_new_session=True
            )
        elif (args.secondaryAction == "stop"):
            pidPath = Path(__file__).resolve().parent / "temp" / "recorderPID"
            try:
                with open(pidPath, "r") as file:
                    psutil.Process(int(file.readline())).terminate()
            except Exception as e:
                print(e)
                pass
        elif (args.secondaryAction == "upload"):
            print("This will upload only the newest output.mkv.")
            print("This will also only create a draft in Lapse. You will have to edit the video manually at lapse.hackclub.com.")
            yarr = input("Are you sure you want to do this? [Y|n]")
            if yarr.lower() == ("n" or "no"):
                print("Upload cancelled. Your video has not been modified.")
            elif yarr.lower() == ("y" or "yes" or "") :
                print("Got it!") 
                utils.upload.initialize()
                utils.upload.beginUpload(api_url)
                
            else:
                print("... Please enter in one of the valid options.")

main()