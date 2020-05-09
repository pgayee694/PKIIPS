# Seer component of PKIIPS

1. Have python3 and pip installed and added to path.
2. Create a virtual environment: `python3 -m venv venv`
3. Source the virtual environment, i.e for Unix: `source env/bin/activate`
4. Install dependencies with `pip install -r requirements.txt`. If the requirements cannot be installed from there, you may have to use your OS's supported packages for OpenCV, numpy, and matplotlib.
5. Perform chessboard calibration to calibrate your stereo camera pair using the script in the calibration directory. Make sure that the generated images are correct, and redo if not. You can also load your own images into the images directory in that folder and direct the script to use those images instead of taking new ones. You will need to use a chessboard that is 9x6 in regards to the interior corners.
6. Adjust the values in seer_config.ini as necessary.
7. Start with `./seers.py`
