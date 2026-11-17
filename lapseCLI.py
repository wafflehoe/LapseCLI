import argparse

from utils.authentication import getAuthToken
from utils.recording import idk 


# Variables
api_url = "https://api.lapse.hackclub.com/api"
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
            getAuthToken(api_url, port)

main()