#!/usr/bin/python

'''
This script is intended to run on the Raspberry Pi Model B
and newer.

@author: Fabien MATHEY
@copyright: Fabien MATHEY
@license: MIT

DISCLAIMER:
I am not liable for any problems this script may cause and
thus it is a "Use at your own risk" typ of thing!
'''

import ConfigParser
import os.path
import time
import subprocess

# Define the Defaults
DEFAULT_SECS = 20
# The script should run every XX settings
SCRIPT_FREQUENCY = 5

# TO ADAPT DEPENDING ON YOUR DISTRO
# show a slide number indicator circl on the top right when slide changes
show_indicator_circl = False
# the following is for Raspbian / Debian based
okular_settings_file = os.path.expanduser("~")+"/.kde/share/config/okularpartrc"
# the following is for archbased
#okular_settings_file = os.path.expanduser("~")+"/.config/okularpartrc"

# put the presentation in the home directory so you can use:
filename = os.path.expanduser("~")+"/presentations/presentation.pdf"
slide_time_file = os.path.expanduser("~")+"/presentations/slide_time.txt"

# secs defines each secoin a slide should be shown before going on
secs=DEFAULT_SECS
# presrun defines if the presentation runs an includes the last modified with unix timestamp
presrun=""
# same as presrun but to discover if the file containing the content for secs
configs=""


# this should run as long as possible
while True:

    # check if the config file exists to get the "secs" from
    if os.path.isfile(slide_time_file):
        # only open the file if there has been a modification
        if configs != os.path.getmtime(slide_time_file):
            with open(slide_time_file, 'r') as f:
                theline = secs
                try:
                    # the secs content should be an int on the first line
                    theline = int(f.readline())
                except:
                    # set the seconds to the DEFAULT_SECS if there has been a problem
                    theline = DEFAULT_SECS

                # if secs in the file is different than the one in the variable, restart the presentation
                # Okular does not dynamically adjust the time a slide is shown, hence a reboot is necessary
                if secs != theline:
                    secs = theline
                    # only restart the presentation if running though
                    if presrun != "":
                        subprocess.call(["killall", "okular"])
                        presrun = ""

            # update the config file with the new secs variable, so Okular knows it.
            config = ConfigParser.ConfigParser()
            # config.optionxform=str
            config.read(okular_settings_file)
            config.set('Core Presentation', 'SlidesAdvanceTime', int(secs))
            # for good measure, tell the presentation to advance and loop (to be sure)
            config.set('Core Presentation', 'SlidesAdvance', True)
            config.set('Core Presentation', 'SlidesLoop', True)
            config.set('Dlg Presentation', 'SlidesShowProgress', show_indicator_circl)
            with open(okular_settings_file, 'w') as configFile:
                config.write(configFile)

            # after saving, update the config variable to prohibit useless calculations
            configs = os.path.getmtime(slide_time_file)


    try:
        # check whether there has been a change to the existing presentation so it can be reloaded
        if presrun != "" and (presrun != os.path.getmtime(filename) or not os.path.isfile(filename)):
            subprocess.call(["killlall", "okular"])
            presrun = ""

        # if there is no running presentation, try to start a presentation
        if presrun == "" and os.path.isfile(filename):
            subprocess.Popen(["okular", "--presentation",filename])
            presrun = os.path.getmtime(filename)

    except:
        # in case someone removes the presentation, just kill okular
        if presrun != "":
            subprocess.call(["killall", "okular"])
            presrun = ""

    # give the machine a little timeout
    time.sleep(SCRIPT_FREQUENCY)
