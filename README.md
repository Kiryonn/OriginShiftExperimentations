## The project
This project provides scripts for experimenting with the Origin-Shift Algorithm for maze generation.
I used it in order to make some experimentations on the Origin Shift Algorithm created by [CaptainLuma](https://github.com/CaptainLuma/).

You will find 2 scripts in particular that you will find useful: "interface_script.py" and "data_only_script.py".

`data_only.py` is a command prompt script and `insterface.pyw` is a GUI tool.

The interface is still a WIP so there might be bugs. Note that it will be completely revamped for better ease of use and
flexibility of testing in the future.

## Installation Guide

- download and install [python](https://www.python.org/downloads/) 3.12 or higher
- during the installation of python, make sure to select the "add to PATH" option
- download the project zip file by clicking on the green button at the top of the github page
![image](https://github.com/user-attachments/assets/2fab4d7a-b8b1-44cb-8a70-5581ad73bbf6)
- unzip the files
- open a terminal
- make sure you are within the same folder as "requirements.txt" (you can change it using `cd [relative_or_absolute_path]`)
- run `python -m pip install -r requirements.txt`

## Usage Guide

### <i>data_only.py</i>

- open a terminal
- run `python data_only.py [commands]`

You can get help by writting `python data_only.py --help`

### <i>interface.pyw</i>

You can just double-click on it. It should open.
commands:
- left-click on a node: select start/end points of the maze
- right-click: add/remove origin
