# What is presentation-pi?

This project is dedicated to bring automatic presentation start and stop for the Raspberry Pi - should work on any linux machine, though.

    DISCLAIMER: USE AT YOUR OWN RISK!

## Criteria to the software

There was a need in my company to run a presentation easily and display them on a screen in the entry hall. As a Raspberry Pi is not really consuming a lot of electricity and thus it was an obvious choice. The following criteria were a requirement:

* Easy to use
* Display one presentation with at least one slide
* Needs to advance through the presentation
* when arriving at the end, it needs to restart
* cheap (free)

Then the obvious: use what you have...

* Raspberry Pi Model B
  - no screen saver
  - no blanking
* Samba Share (Windows Share)
* SSH connection for distance connection (The pi is in a different room than the screen)

## Which models are supported?

This should work on every Raspberry Pi running Raspbian Wheezy but it has been tested on a Raspberry Pi Model B.

## Configuring the Pi

The configuration is based upon a local installation. This means that you have a keyboard, mouse attached and a screen attached to be able to configure the pi directly.

### create folders and permissions

If you want to use the provided script as is, you should create a folder ```presentations``` in the root folder ```/home/pi/```. Then you need to give it the permissions to be used by everyone ```chmod 777 presentations```

Then you need to install the **SSH server** and the **Samba server**. Please consult the official documentation on how to install and configure this. And obviously, the ```presentations``` folder is the one to be shared.

Create a file ```slide_time.txt``` in the presentations folder and edit it. It should only contain an integer value. That integer states the number of seconds each slide should be visible - we used ```20```.

The actual presentation should be called "presentation.pdf" and placed into the root of the shared folder.

### Install okular (and screen for ssh)

Okular is a wonderful tool when it comes to PDF presentations. That allows us to have the automatic progression through and loop the presentation. The python script will take care of the configuration of the ```slide advance time```, ```advance slide``` and loop settings.

Screen is used to be able to start scripts that run in the background manually so that you can disconnect from the pi without killing the script.

### Configure the X

As the Raspberry Pi is by default blanking after a set amount of time, we need to deactivate that. So start by installing ```xscreensaver```, run it and disactivate the screen saver. Do not uninstall it afterwards as the blanking would come back. Additionally, you need to configure your ```.profile``` by adding the following lines at the end, if you desire to run the script via ssh:

```bash
export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=':0'
```

This is needed to tell the okular to which display to bind to as there is no default set.

Then you need to set the following in the file ```/etc/xdg/lxsession/LXDE/autostart```

```bash
@xset s noblank
@xset s off
@xset -dpms
```

### Copy the scripts

Copy the provided scripts, ```runner.py``` and ```afterstart.sh``` to the pi root directory ```/home/pi/```. Remember that you can modify them as you please - it is under MIT license...


## Running the show

now that you are set up, you can add a desktop background (like a company logo) and then power down the machine. Once powered down, you can move the pi to the final location, plug the network cable and HDMI in an let it run.

Once the system booted, you can connect to the Pi via SSH and run the scripts (copied in the the root directory).

### afterstart.sh

That script actually kills the taskbar and runs the python script using screen in detached mode. If you want to run just the script without the removal of the taskbar, comment the line ```killall lxpanel``` (using a #).

It runs!

## How to use

Anyone having the user and password to access the share can change the presentation. It is important to note that the the presentation is relaunched automatically after one has copied a new presentation or modified the time. It is also important to not that every operation might take a lot of time as we are talking about a Raspberry Pi.

If you delete the ```presentation.pdf``` or ```slide_time.txt``` the script will not die. It will stop the presentation or simply reset the time to the ```DEFAULT_SECS``` in the ```runner.py```.

But all that has to be done by the user is to connect to your *windows share* on the Raspberry Pi and copy the file. The rest is handled automatically.

## Troubleshooting

If the presentation does not start, ever if you files are all in the correct place, please verify that the script is actually running. If you ran it using the provided ```afterstart.sh```, then you can check simply by writing ```screen -r presentation```. If nothing turns up, than consider rerunning the script or starting the command manually.
