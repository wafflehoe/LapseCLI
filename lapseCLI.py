import argparse
import psutil

from pathlib import Path


import subprocess
import sys

import utils.authentication


# Variables
lapse_api_url = "https://api.lapse.hackclub.com/api"
lookout_api_url = "https://lookout.hackclub.com/api"
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
        match args.secondaryAction:
            case "token":   
                utils.authentication.getAuthToken(lapse_api_url, port)
        # if (args.secondaryAction == "token"):
        #     utils.authentication.getAuthToken(api_url, port)
        # elif (args.secondaryAction == "register"):
        #     utils.authentication.registerDevice(api_url)
        #     pass
        # elif (args.Seco)
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

main()