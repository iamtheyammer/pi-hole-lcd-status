# Pi-Hole LCD Status

Shows the status of your Pi-Hole on a (right now) 16x2 character I2C LCD display.

## Table Of Contents

- [Just run](#just-run)
- [Build and run](#build-and-run-more-difficult-more-involved)
- 

## Just run

1. Go to your home folder `cd ~`
2. Enable I2C communication `sudo raspi-config`, `Interfacing Options`, `I2C`, `Enable`
3. Install docker and add pi to the `docker` group `curl -sSL https://get.docker.com | sh && sudo usermod -a -G docker pi`
4. Reboot `sudo reboot 0`
5. Set up environment variables
    1. Open the env file `nano pi_hole_lcd_status_env.txt`
    2. Add these lines:
        - `PIHOLEMON_HOSTNAME=<http/https>://<pi-hole-ip>`, ex: `PIHOLEMON_HOSTNAME=http://1.1.1.1`
    3. Exit `nano` (ctrl+x, Y)
6. Edit your `rc.local` file (makes this run at startup) `sudo nano /etc/rc.local`
7. Fetch the container `docker pull iamtheyammer/pi-hole-lcd-status:latest`
8. Before the `exit 0`, add `docker run -d --privileged --env-file /home/pi/pi_hole_lcd_status_env.txt iamtheyammer/pi-hole-lcd-status:latest`
    - If you want the container to automatically be kept up to date, add the command from step 7 before the above command.
    Note that this may make boot slower when a new version is available.
9. Reboot to see it work! `sudo reboot 0`

## Build and run (more difficult, more involved)

First, follow these steps to get started:

1. Go to your home folder `cd ~`
2. Clone this repo into it `git clone https://github.com/iamtheyammer/pi-hole-lcd-status.git`
3. Enable I2C communication `sudo raspi-config`, `Interfacing Options`, `I2C`, `Enable`
4. Reboot `sudo reboot 0`
5. Follow a guide below to install and run

### Docker (easiest, minimal performance hit)

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

### Updating

To update, just git pull from the `pi-hole-lcd-status` directory (`git pull origin master`) and reboot.

## Errors# Pi-Hole LCD Status

Shows the status of your Pi-Hole on a (right now) 16x2 character I2C LCD display.

## Table Of Contents

- [Just run](#just-run)
- [Build and run](#build-and-run-more-difficult-more-involved)
- 

## Just run

1. Go to your home folder `cd ~`
2. Enable I2C communication `sudo raspi-config`, `Interfacing Options`, `I2C`, `Enable`
3. Install docker and add pi to the `docker` group `curl -sSL https://get.docker.com | sh && sudo usermod -a -G docker pi`
4. Reboot `sudo reboot 0`
5. Set up environment variables
    1. Open the env file `nano pi_hole_lcd_status_env.txt`
    2. Add these lines:
        - `PIHOLEMON_HOSTNAME=<http/https>://<pi-hole-ip>`, ex: `PIHOLEMON_HOSTNAME=http://1.1.1.1`
    3. Exit `nano` (ctrl+x, Y)
6. Edit your `rc.local` file (makes this run at startup) `sudo nano /etc/rc.local`
7. Before the `exit 0`, add `docker run -d --privileged --env-file /home/pi/pi_hole_lcd_status_env.txt iamtheyammer/pi-hole-lcd-status:latest
8. Reboot to see it work! `sudo reboot 0`

This will automatically be kept up to date, because docker will check that the current build is latest before running it.

## Build and run (more difficult, more involved)

First, follow these steps to get started:

1. Go to your home folder `cd ~`
2. Clone this repo into it `git clone https://github.com/iamtheyammer/pi-hole-lcd-status.git`
3. Enable I2C communication `sudo raspi-config`, `Interfacing Options`, `I2C`, `Enable`
4. Reboot `sudo reboot 0`
5. Follow a guide below to install and run

### Docker (easiest, minimal performance hit)

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

### Updating

To update, just git pull from the `pi-hole-lcd-status` directory (`git pull origin master`) and reboot.

## Errors

So you've encountered an error. Use the table below to debug.

| Error Code/Issue | Description |  
| ---------------- | ----------- |  
| Nothing on the screen | You may be using an incompatible screen I2C may not be enabled. |  
| The screen went blank from working | The docker container may have stopped. Try rebooting. |  
| 0 | You're missing a required environment variable, see the install section you used for more. |  

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

So you've encountered an error. Use the table below to debug.

| Error Code/Issue | Description |
| :========= | :========== |
| Nothing on the screen | You may be using an incompatible screen I2C may not be enabled. |
| The screen went blank from working | The docker container may have stopped. Try rebooting. |
| 1 | You're missing a required environment variable, see the install section you used for more. |
| 2 | There was an issue with the request for data. Make sure that the `PIHOLEMON_HOSTNAME` environment variable is correct. |

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)