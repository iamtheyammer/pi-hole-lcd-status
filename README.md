# Pi-Hole LCD Status

Shows the status of your Pi-Hole on a (right now) 16x2 character I2C LCD display.

## Run

First, follow these steps to get started:

1. Go to your home folder `cd ~`
2. Clone this repo into it `git clone https://github.com/iamtheyammer/pi-hole-lcd-status.git`
3. Enable I2C communication `sudo raspi-config`, `Interfacing Options`, `I2C`, `Enable`
4. Reboot `sudo reboot 0`
5. Follow a guide below to install and run

### Docker (easiest, minimal performance hit)

Note: I will push this to docker hub at some point in the future, but for now it's ok just to build it

1. Install docker and add pi to the `docker` group `curl -sSL https://get.docker.com | sh && sudo usermod -a -G docker pi`
2. Go into the folder `cd pi-hole-lcd-status`
3. Make environment variables `make buildenv`
4. Build the docker container `make dockerbuild`
5. Run the container as a daemon `make dockerrund`

#### Running on startup (docker)

1. Edit your `rc.local` file `sudo nano /etc/rc.local`
2. Before the `exit 0`, add `cd /home/pi/pi-hole-lcd-status && make dockerrund` (modify if your path is different)
3. Done: reboot to see the changes immediately take effect

### Manual (harder, but lower performance hit)

1. Enter the cloned folder `cd pi-hole-lcd-status`
2. Install deps `make install`
3. Make environment variables `make buildenv`
4. Add the `export ` key before each env var in `docker_env.txt`, using something like nano (and edit the env vars, if needed)
5. Enter the python virtual environment `source bin/activate`
6. Run the tool `python3 src/main.py`

#### Running on startup (manual)

1. Install the screen command `sudo apt-get update && sudo apt-get install screen`
2. Edit your `rc.local` file `sudo nano /etc/rc.local`
3. Before the `exit 0`, add `source cd /home/pi/pi-hole-lcd-status && source docker_env.txt && source bin/activate && python3 src/main.py`
4, Done: reboot to see the changes immediately take effect

## Update

To update, just git pull from the `pi-hole-lcd-status` directory (`git pull origin master`) and reboot.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)