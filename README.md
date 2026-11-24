# LapseCLI

LapseCLI is a command line interface that allows for recording timelapses from the command line.

## Installation

1. Clone the GitHub repository from source and enter the folder using
```bash
git clone https://github.com/wafflehoe/LapseCLI.git
cd LapseCLI 
```
2. Run `pip install -r requirements.txt`
3. Run `python ./lapseCLI.py` with the arguments found below.

>[!NOTE]
>The earliest version of Python required is 3.15. Please make sure your Python version is up to date before making an issue request.

>[!NOTE]
>On non-Windows PCs, you may need to give your terminal access to take photos of your screen. This is used only to send data directly to Lookout.

## Usage

`python ./lapseCLI.py (config|timelapse) <action>`

Before you begin using the CLI, you must authenticate with your Hack Club account. This can be done by using `python ./lapseCLI.py config authenticate`, which will open a web browser asking you to accept certain permissions. Once you enter it, ./config/userConfig.json will update with your token.

> [!CAUTION]
> The token received will be stored *in plaintext.* It is recommended to remove your token after you are finished to prevent someone from gaining full access to your account.

From there, you can use the following commands to interact with Lapse.

### config
* **authenticate**
	Open an OAuth2 prompt to obtain a token to your account.

* **whoami**
	Tells you basic information about yourself. 
	This is the only reason I ask for the "user:read" scope, by the way

### timelapse
* **record**
	Begins a recording.
	Runs in the background, takes a screenshot once a minute.

* **stop**
	Stops the current recording.

* **pause**
	Pauses the current recording.
	When paused, a recording cannot be stopped.

* **resume**
	Resumes the current recording.
	... yeah. This can only be used with an active recording.
 
