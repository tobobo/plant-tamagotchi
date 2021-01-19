## Hardware

- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/). This should (probably) work with any Pi, but the Zero is a good size. I'm not a very confident solderer, so I got a [Zero WH](https://www.raspberrypi.org/blog/zero-wh/).
- Some kind of micro SD card to store the data for the Pi, and a way to copy data to it—maybe a Micro SD to SD card adapter, and an SD card reader if your computer doesn't have one.
- [2.13" E-Ink Display for Raspberry Pi](https://www.seeedstudio.com/2-13-Triple-Color-E-Ink-Display-for-Raspberry-Pi-p-4044.html)
- [Capacative moisture sensor](https://www.seeedstudio.com/Grove-Capacitive-Moisture-Sensor-Corrosion-Resistant.html)
- [Grove base HAT for Raspberry Pi Zero](https://www.seeedstudio.com/Grove-Base-Hat-for-Raspberry-Pi-Zero.html)

## Assembly

### Display setup

I found it a bit tricky to connect the display to the board—it's kind of a flimsy ribbon cable that you need to push pretty firmly in to its connector.

### Grove HAT + moisture sensor

The capacative moisture sensor is an analog sensor. Connect it to port A0 on the Grove base HAT.

### Putting it all together

You should be able to stack the Grove HAT and E-Ink display. First push the Grove HAT (with the moisture sensor attached) in to the Pi, and then push the E-Ink display in to the Grove Hat's 40 pin connector. They don't fit as snug as they could, but it should make sufficient contact for everything to work.

## Raspberry Pi setup

### Prerequisites

I used the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to put a Raspberry Pi OS Lite image on the Pi. In order to be able to SSH to the Pi, I also added the following files to the SD card before inserting in to the Pi.

- [A `wpa_supplicant.conf` file](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) so that the Pi will connect to the desired Wi-Fi network.
- [An empty `ssh` file (see "Enable SSH on a headless Raspberry Pi")](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) to enable SSH access when the Pi boots.

### Python libraries

After SSHing in to your Pi (by default you should be able to do `ssh pi@raspberrypi.local` with password `raspberry`, which you'll be prompted to change), you'll need to do some initial setup to install the libraries that allow all the hardware to work.

#### E-Ink

- Complete the "Enable SPI Interface" and "Libraries Installation" steps (on the "Hardware/Software setup" page) from the [Waveshare 2.13" e-Paper HAT guide](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B)). Be sure to use the Python 3 instructions.
- If you'd like to download and run the examples (not necessary to build this project), you'll need to change the pin definitions [as described in this guide](https://www.raspberryconnect.com/projects/42-hardware-addons/177-the-seeed-studio-e-ink-2-13-inch-3-colour-display-python-guide). For the E-Ink display I used, the [epd_2in13bc_test.py](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/examples/epd_2in13bc_test.py) file worked.

#### Moisture sensor

- Use the Python 3 steps to [install Seeed Studio's Grove.py library](https://github.com/Seeed-Studio/grove.py#install-grovepy).
- You can test that you're getting readings from your moisture sensor by running the `grove/grove_moisture_sensor.py` file—note that the default ranges seem to be off in my tests, they may be for a resistive moisture sensor (the output of the above file will always read "wet").

### Setting up this respository.

You do not need to clone this respository to your Raspberry Pi—the deploy script can be used to sync your code from your development computer to the Pi so you can easily iterate on the code.

