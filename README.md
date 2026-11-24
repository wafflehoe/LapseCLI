# LapseCLI

> *"LapseCLI is the best recorder I've ever used."* — Albert Einstein, 1667

LapseCLI is a command line interface that allows for recording timelapses from the command line.

## Installation

There are currently two ways of installing LapseCLI. One of them is from source, and the other is from pip.

### From pip

1. Install this GitHub repo with this command:
```bash
pip install "git+https://github.com/wafflehoe/LapseCLI.git"
```
2. Wait for it to finish installing all dependencies.
3. Run `lapseCLI` with the arguments found below.

### From source

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

> *If you are using the pip version, replace `python ./lapseCLI.py` with `lapseCLI`*

Before you begin using the CLI, you must authenticate with your Hack Club account. This can be done by using `python ./lapseCLI.py config authenticate`, which will open a web browser asking you to accept certain permissions. Once you enter it, `./config/userConfig.json` will update with your token.

> [!CAUTION]
> The token received will be stored *in plaintext.* It is recommended to remove your token after you are finished to prevent someone from gaining full access to your account.

From there, you can use the following commands to interact with Lapse.

### config
- **authenticate**
	- Open an OAuth2 prompt to obtain a token to your account.

- **whoami**
	- Tells you basic information about yourself. 
	- This is the only reason I ask for the "user:read" scope, by the way

- **deleteToken**
	- Replaces the token saved at `./config/userConfig.json` with a placeholder.
	- You will need to re-run authenticate after this.

### timelapse
- **record**
	- Begins a recording.
	- Runs in the background, takes a screenshot once a minute.
	- This will not stop with the closing of the terminal, please remember to use the stop command.
	- The recording may crash if your internet crashes during an image upload.

- **stop**
	- Stops the current recording.
	- This instantly sends a draft to Lapse. Be careful not to show any secrets, as editing is not supported.

- **pause**
	- Pauses the current recording.
	- When paused, a recording cannot be stopped.

- **resume**
	- Resumes the current recording.
	- ... yeah. This can only be used with an active recording.
 
