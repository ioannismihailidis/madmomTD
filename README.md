# madmomTD
AI based beatdetection for touchdesigner build around https://github.com/CPJKU/madmom/ \

# Features
- Easy one click dependencies installer
- stable beat detection from a selected audio input device

## Requirements
- TouchDesigner 2023.xxxx
- Windows 10/11
- python 3.9  https://www.python.org/downloads/release/python-395/
- Mic/LineIn Device

## How to install
- Install Python 3.9

- **Caution**: tox/toe are marked as LFS. Please use the download from releases or clone with git. "Download zip" won't pull the lfs files and you will have corrupted touchdesigner files! \
![image](https://github.com/ioannismihailidis/madmomTD/assets/1242010/4f02c655-bfb8-4a22-be72-561e5b5667bd)

- Open madmom.toe. "Install" creates a virtual enviroment in the selected basefolder and installs all needed dependencies \
![image](https://github.com/ioannismihailidis/madmomTD/assets/1242010/8c8d7e52-df57-46c5-9614-3a8b6dd6b771)

## How to use
- Select unter "Control" the audio input device and click "start" \
![image](https://github.com/ioannismihailidis/madmomTD/assets/1242010/ccb8d196-10c8-423d-b0b2-580a7b6098e8)

- A prompt opens, activates the created environment and starts the madmom beatdetection. Internally the beat will be passed from the python script to touchdesigner via osc. \
![image](https://github.com/ioannismihailidis/madmomTD/assets/1242010/1387233c-74d3-475f-b42f-e9f4454742d1)


## Todos
- MacOS Support
- Add time signature options
- Add parameters, thresholds, etc. for beatdetection
- Beat post processing
- Fix halfstep beatdetection: E.g. Drum and bass track are detected with 88 and not 176 bpm.
