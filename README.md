## The project
This project provides scripts for experimenting with the Origin-Shift Algorithm for maze generation.
I used it in order to make some experimentations on the Origin Shift Algorithm created by [CaptainLuma](https://github.com/CaptainLuma/).


## Scripts
You will find 2 scripts in particular that you will find useful: "interface_script.py" and "data_only_script.py".

"data_only.py" will let you manipulate a maze through the given functions. You will find an example in it to show how you can use the functions in order to manipulate the maze.

"interface_script.py" will let you vizualize what happens with control over the number of step, the size of the maze, the visualization of the solution, the manipulation of the start/end nodes throught left click on a node, the creation/deletion of origins through the right click on a node and the capture of the current state of your maze into an image. More QoL might be added in the future.


## Install
If you don't have git or python, you have to download them:
- git: https://git-scm.com/downloads
- python (3.10 or higher): https://www.python.org/downloads/

You can directly install the environment using the following commands:
- `git clone https://github.com/Kiryonn/OriginShiftExperimentations.git <your-folder-path>`
- `cd <your-folder-path>`
- `python -m venv .venv`
- windows: `.\.venv\Scripts\activate`
- linux/macos: `source .venv/bin/activate`
- `pip install -r requirements.txt`


<br>
The data_only_script.py doesn't require any dependency other than python 3.

You will also need an IDE such as Visual Studio Code, Pycharm Community, or any other that you like to manipulate those files.

## Additional work
If you want to create scripts based on my work, please fork the project, or mention this repository in the README.md file of your own github repository.
