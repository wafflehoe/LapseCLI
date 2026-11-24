import argparse
import psutil

from pathlib import Path


import subprocess
import sys
import os

def main():
    # fix issues with pip
    currentPath = os.path.dirname(os.path.abspath(__file__))
    if (currentPath not in sys.path):
        sys.path.insert(currentPath)
        
    import utils.authentication
    import utils.recording
    
    # Variables
    lapse_api_url = "https://api.lapse.hackclub.com/api"
    port = 8081

    parser = argparse.ArgumentParser(description="Interact with Lapse without Lookout.")

    # TODO: add arguments
    parser.add_argument("option", type=str, help="")
    parser.add_argument("secondaryAction", type=str)

    args = parser.parse_args()

    if (args.option == "config"):
        match args.secondaryAction:
            case "authenticate":   
                utils.authentication.getAuthToken(lapse_api_url, port)
            case "whoami":
                utils.authentication.whoami(lapse_api_url)
            case "deleteToken":
                utils.authentication.wipeToken()
    elif (args.option == "timelapse"):
        match args.secondaryAction:
            case "record":
                subprocess.Popen(
                    [sys.executable, "-m", "utils.recording"],
                    start_new_session=True
                )
            case "stop":
                pidPath = Path(__file__).resolve().parent / "temp" / "recorderPID"
                try:
                    with open(pidPath, "r") as file:
                        psutil.Process(int(file.readline())).terminate()
                except Exception as e:
                    print(e)
                    pass
                utils.recording.stopRecording()
            case "pause":
                utils.recording.pauseRecording()
            case "resume":
                utils.recording.resumeRecording()

main()