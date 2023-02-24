# AmiiPi

This is a Python project to use RPi 0w with OLED hat to work with Proxmark3, acting as an Amiibo emulator.

## Disclaimer

## Feature

This is basically an UI for Proxmark3 RRG firmware. It can:

- Select Amiibo dump to load by filters, including characters, game series and usable game.
- Select within filters by initials.
- Display basic Amiibo information
- Easy loading dumps, randomizing UID, and saving data in Proxmark3 memory back to RPi.
- Support both cable connection (USB serial device) or Blueshark plugin (Bluetooth serial device).
- Could be modified to work with other projects, as long as it can be run from Python. Either it's Python project, or have standard format to interact with.
- Support for long names with rolling title display.

It cannot:

- Write Amiibo tags. This project is not designed for this, and I don't see why I need to add this. A phone with NFC is enough to do this.
- Give you Amiibo dumps. Please dump your own or find them yourselves.

Any feature request or suggestion is welcomed, as long as I have the hardware to work with.

## Hardware setup

> The hardware build of this system is versatile. Another build may be compatible with minimum modification.

This project requires the following hardware to work:

- Raspberry Pi 0w. Other compatible single board computers, like other RPi models, also works, if it has sufficient processing power, RAM, SPI interface and compatible GPIO layout.
- Waveshare 1.3 inch OLED HAT. Other OLED display requires at least modification to ``Interface.py`` to accomodate the hardware difference.
- RRG firmware comparible Proxmark3. Other hardwares may be needed for it to connect to RPi,like MicroUSB to USB connector, Blueshark, etc.
- (Recommended) UPS or battery pack for Raspberry Pi.
- Other necessary components, like Micro SD card, card reader, ethernet cable, etc.
- Amiibos. Legally speaking, you can only dump the Amiibos you own, and use them with this project. I will not be providing the cryptographic key, the Amiibo dumps, nor the ways to dump the Amiibos. However, Google is always your friend. There're plenty of tutorials on how to dump your Amiibos.

## Installation

Assume that you're using latest Raspberry Pi OS (previously called Raspbian), and have access to Internet. Refer to official guide on how to set up RPi, connect to Internet, SSH into the RPi, etc.

### Install necessary libraries

Run:

```shell
sudo apt -y install git ca-certificates build-essential pkg-config libreadline-dev gcc-arm-none-eabi libnewlib-dev qtbase5-dev libbz2-dev libbluetooth-dev libpython3-dev libssl-dev
```

To install necessary libraries from apt.

### Set up and build Proxmark3 client

Refer to their official documents for more details.

First pull the repository:

```shell
git clone https://github.com/rfidresearchgroup/proxmark3.git
```

Then start the build:

```shell
cd proxmark3
make accessrights
make clean && make all -j
sudo make install
```

If necessary, flash the new firmware into Proxmark3:

```shell
./pm3-flash-all
```

### Set up this project

First pull the repository:

```shell
git clone https://github.com/firefox2100/AmiiPi.git
```

Set up the Python invironment:

```shell
cd AmiiPi
python3 -m pip install -r requirements.txt
```

Prepare the Amiibo dumps. To make the indexing easier, this project requires the dumps to be named as ``head-tail.bin``, where ``head`` and ``tail`` is the 8 bytes ID in Amiibo data. Detailes of this can be queried with [AmiiboAPI](https://amiiboapi.com). To make preperations easier, a script called ``Rename.py`` is provided with this project. Simply put your dumps in the same folder (it's OK to have subfolders in it) and run:

```shell
python ./src/Rename.py -i <path/to/your/dumps/> -o <path/to>./assets/amiibos/
```

Copy the key to the assets folder. The key file should be one combined file, although 2 separate files are also acceptable, with modification to the code.

Configure the paths. Open ``src/Proxmark3.py``, and modify the path strings to fit your system.

```text
proxmark_path = "Path to your proxmark3 project folder"
port = "Bluetooth port or serial port"
amiibo_path = "Path to your Amiibos folder"
key_path = "Path to the key"
```

Enable the SPI function through ``raspi-config``. If your hardware or distro is different, refer to corrisponding document on how to enable SPI.

Modify and install the amiipi.service, if you need it to be started on boot.

Afterwards, simply connect (or turn on, depending on whether the bluetooth is used) the Proxmark3, and run ``AmiiPi.py``
