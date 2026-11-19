#for RECORDING!!! Finally!
from mss import MSS
import imageio
import imageio_ffmpeg
from PIL import Image
import asyncio
import time
import numpy

# config stuff
from pathlib import Path
import json


recording = False
recordingFPS = 6

outputPath = Path(__file__).resolve().parent.parent / "temp" / "output.mkv"
writer = None

config = None

# writes image to video stream
def writeVideo(screenshot):
    writer.append_data(imageio.core.util.Image(numpy.array(screenshot)[:,:,:3][:,:,::-1]))

# loop that actually records video
# TODO: make this able to be stopped with another command
def beginRecording():
    if (not writer):
        print("Something went wrong, and the video writer did not start.")
        return
    try:
        with MSS() as sct:
            while True:
                time.sleep(1/recordingFPS)
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                writeVideo(screenshot)
    except KeyboardInterrupt:
        print("Oop.")
    finally:
        writer.close()



def initialize():
    global recordingFPS
    global outputPath
    global writer
    try:
        configPath = Path(__file__).resolve().parent.parent / "config" / "recordingConfig.json"
        with open (configPath, "r") as data:
            config = json.load(data)
        recordingFPS = config["recordingFPS"]
        print(recordingFPS)
    except Exception as e:
        print(e)
        print("Recording config doesn't exist or is corrupted. Using defaults.")

    writer = imageio.get_writer(
        outputPath,
        fps=recordingFPS, 
        quality=4, 
        codec="libx264",
        ffmpeg_params=[
            "-crf", "32",
            "-preset", "slow",
            "-pix_fmt", "yuv420p"
        ]
    )
