**Week 2 : Media Acquisition**

Objective: Learn how to capture images, videos, and sound.

Instructions:

1. Copy and test the following sample programs.
2. If you have not installed the package in the previous week, please install run the following line in the terminal or powershell.

**Package: OpenCV**

pip install opencv-python

Reference materials: [OpenCV: Video I/O](https://docs.opencv.org/4.x/dd/de7/group__videoio.html)

**Capturing image**

* Create a new python file

import cv2

* initialize the videoCapture object.

cam = cv2.VideoCapture(0) # create webcam object

* Check whether the computer camera can be used or not.

if not cam.isOpened():

    print("not able to open computer camera")

    exit()

* Start loop to keep capturing the image from the camera.
* The loop will stop (destroy the window) once the user press ‘q’ or write to file when user press ‘c’

while True:

result, image = cam.read() # start to capture frame by frame

cv2.imshow(‘Captured Image’, image) # show the UI for us to see

# unicode code of a specified character.

If cv2.waitKey(1) == ord(‘c’): # key press -c

        cv2.imwrite(“myimage.png”,image)

elif cv2.waitKey(1) == ord(‘q’): # key press q

break

cv2.destroyAllWindows()

* Stop the camera

# Release the camera (close)

cam.release()

**Capturing Video**

Note: You can modify the previous code or create a new file for this program.

import cv2

cam = cv2.VideoCapture(0) # create webcam object

You need to create the video file.

#create video file and format.

fourcc = cv2.VideoWriter\_fourcc(\*'XVID')

videoWriter = cv2.VideoWriter('myvideo.avi', fourcc, 20.0, (640,  480))

***function:*** [***OpenCV: cv::VideoWriter Class Reference***](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html)

if not cam.isOpened():

    print("not able to open computer camera")

    exit()

while True:

    result, image = cam.read() # start to capture frame by frame

    if not result:

        print("Not able to capture frame (stream ending)")

cv2.imshow('Captured Image', image) # show the frame (image)

Continuous recording the video until user press ‘q’

if not cam.isOpened():

    print("not able to open computer camera")

    exit()

while True:

# Wait for user input, press any key to close the window

cv2.destroyAllWindows()

# Release the camera (close)

cam.release()

**Sound Recording**

Library required: Pyaudio and wave

Install the library.

* pip install Pyaudio
* pip install wave

Reference:

* [PyAudio · PyPI](https://pypi.org/project/PyAudio/)
* [Wave · PyPI](https://pypi.org/project/Wave/)
* Create a new python file to record the sound

import pyaudio

import wave

* Set the parameter for recording

chunk = 1024

format = pyaudio.paInt16  # Audio format

channel = 1  #audio channel (1 - mono, 2 - stereo)

rate = 44100  # Sample rate per second

second = 5  # Duration

outputWaveFile = "mysound.wav"

available format: [**paFloat32**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paFloat32), [**paInt32**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paInt32), [**paInt24**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paInt24), [**paInt16**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paInt16), [**paInt8**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paInt8), [**paUInt8**](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.paUInt8),

* Create the pyaudio object for recording

# Initialize PyAudio

p = pyaudio.PyAudio()

* Create the stream object for recording, calling the function open.

#  stream for recording

stream = p.open(format=format,

                channels=channel,

                rate=rate,

                input=True,

                frames\_per\_buffer=chunk)

Parameters for audio stream open function:

* **rate** – Sampling rate
* **channels** – Number of channels
* **format** – Sampling size and format. See [PortAudio Sample Format](https://people.csail.mit.edu/hubert/pyaudio/docs/#pasampleformat).
* **input** – Specifies whether this is an input stream. Defaults to False. (recording-so use input)
* **frames\_per\_buffer** – Specifies the number of frames per buffer.

Create a frame to store the audios.

Loop for certain number of times to record the chunk (1024) into list (frames)

* 44100/1024\*5 = 215 , so total iteration is 215 .

frames = []

print("\* Recording started...")

# read audio data to frames

for i in range(0, int(rate / chunk \* second)):

    data = stream.read(chunk)

    frames.append(data)

print("\* Recording finished.")

* Once finished recording, stop the services by stopping and close the streaming and following by deleted the audio object.

stream.stop\_stream()

stream.close()

# Terminate PyAudio object

p.terminate()

* Write the frames list into the file. You still need to set the channel (mono / stereo), framerate and format.

# Save the audio data to WAV file

wf = wave.open(outputWaveFile, 'wb')

wf.setnchannels(channel)

wf.setsampwidth(p.get\_sample\_size(format))

wf.setframerate(rate)

wf.writeframes(b''.join(frames))

wf.close()

print("completed")

**Screen Recording**

Another library required: pyscreenrecorder

* pip install pyscreenrecorder

References : [GitHub - SSujitX/pyscreenrecorder: A python screen recording package with customizable resolution, FPS, and mouse tracking.](https://github.com/SSujitX/pyscreenrecorder)

* Import the screenRecorder module from pyscreenrecorder library

from pyscreenrecorder import ScreenRecorder

* Call the screenRecorder function and set all the parameters.

print("start....")

ScreenRecorder(

    filename="examplewithPyScreenRecorder.mp4",

    duration=5,

    fps=60,

    monitor\_number=1,

    resolution=(1280, 720),  # Set custom resolution

    mouse=True,

    mouse\_color=(255, 0, 0),  # Red cursor

    mouse\_size=10,

    mouse\_thickness=3,

)

print("done")

Parameter list in the ScreenRecorder Function:

* + filename= file name
  + duration= duration for the recording
  + fps= frame per seconds,
  + monitor\_number= monitor set to 1, if you have more than 1 monitor then you can set it to other monitor example 2.
  + mouse= allow mouse tracking
  + resolution = the screen / display resolution

E**xercise**

Write a program to capture the video (live camera or screencapture) with sound, you may use any library that are listed on pypi site.
