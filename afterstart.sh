# This script is intended to run on the Raspberry Pi Model B
# and newer.

# @author: Fabien MATHEY
# @copyright: Fabien MATHEY
# @license: MIT

# DISCLAIMER:
# I am not liable for any problems this script may cause and
# thus it is a "Use at your own risk" typ of thing!

# the following needs to be done after boot:
# No root required

# remove the top bar from the screen (Taskbar)
killall lxpanel

# run the script in the background
screen -dmS presentation ./runner.py
