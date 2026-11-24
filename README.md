> "Imagine a really deep quote here." - Albert Einstein.

# LapseCLI

LapseCLI is a command line interface that can interact with Hack Club's Lapse. This allows you autonomously interact with Lapse, which could be useful in a variety of ways. 

### Installation:

1. Clone the GitHub repository from source. 
2. Enter into the folder.
3. Run `python -m venv venv`
4. Run ./lapseCLI.py with the arguments found below.

>[!NOTE]
>This script... requires Python. I developed it on 3.15.2, but I am willing to make it compatible with 3.14 if the demand exists.

### Usage

`./lapseCLI.py (config/timelapse/user) (secondaryAction) --token [TOKEN]

Before you begin using the CLI, you must authenticate with your Hack Club account. This can be done by using `[config] [authenticate]`, which will open a web browser asking you to accept certain permissions. Once you enter it, ./config/userConfig.json will update with your token.

> [!CAUTION]
> The token received will be stored *in plaintext.* It is recommended to remove your token after you are finished to prevent someone from gaining full access to your account.

From there, you can use the following commands to interact with Lapse.

config
* authenticate
	Open an OAuth2 prompt to obtain a token to your account.

* whoami
	Tells you basic information about yourself. 
	This is the only reason I ask for the "user:read" scope, by the way
timelapse
* record
	Begins a recording.
	Runs in the background, takes a screenshot once a minute.

* stop
	Stops the current recording.

* pause
	Pauses the current recording.
	When paused, a recording cannot be stopped.

* resume
	Resumes the current recording.
	... yeah.
 
