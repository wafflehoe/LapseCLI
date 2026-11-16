import argparse

import httpx2
from authlib.integrations.httpx_client import AsyncOAuth2Client
import os

#for auth code retrieval
import threading
import http.server
import socketserver

#for PKCE
import secrets
import hashlib
import base64

# Variables
api_url = "https://api.lapse.hackclub.com/api"
auth_url = "https://hackatime.hackclub.com"
port = 8081

parser = argparse.ArgumentParser(description="Interact with Lapse without Lookout.")

# TODO: add arguments
parser.add_argument("option", type=str, help="")
parser.add_argument("secondaryAction", type=str)

args = parser.parse_args()

def generatePKCE():
    code_verifier = secrets.token_urlsafe(64)
    print(code_verifier)
    sha256 = hashlib.sha256(code_verifier.encode('utf-8')).hexdigest()
    code_challenge = base64.b64encode(sha256.encode("utf-8"))
    return (code_verifier, code_challenge)

def getClientId():
    return "svc_aa5b7136e4e4f5472d896e23"

def getAuthToken():
    client_id = getClientId()
    code_verifier, code_challenge = generatePKCE()
    client = AsyncOAuth2Client(
        client_id=client_id, 
        code_challenge_method="S256", 
        redirect_uri="http://localhost:8081", 
        scope="timelapse:read timelapse:write snapshot:read snapshot:write")
    uri, state = client.create_authorization_url(api_url + "/auth/authorize", code_verifier=code_verifier)
    print(uri)



    # start HTTP server to retrieve auth code
    authorizationCode = None

    class authorizationHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            print(self.path)

            self.server.auth_code = self.path.split("?")[1].split("=")[1].split("&")[0]
            # TODO: stop csrf attacks or somethiing like that? idk.
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            
            


    os.startfile(uri)
    httpd = socketserver.TCPServer(("", port), authorizationHandler)
    httpd.serve_forever()
    authorizationCode = httpd.auth_code
    if (not authorizationCode):
        print("Authorization code was never gotten, please run again!")
        return
    
    print(authorizationCode)

    # get token from auth code
    response = httpx2.post(
        api_url + "/auth/token", 
        data={
            "client_id": client_id,
            "code": authorizationCode, 
            "redirect_uri": "http://localhost:8081", 
            "grant_type": "authorization_code", 
            "code_verifier": code_verifier,
            "client_secret": ""
            },
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        )

    print(response.text)
    pass

def main():
    print(args)
    if (args.option == "config"):
        if (args.secondaryAction == "token"):
            getAuthToken()

main()