# CO2meter

CO2meter is a Python interface to the USB CO2 monitor with monitoring and logging tools, flask web-server for visualization and Apple HomeKit compatibility.


# Installation

### Prerequisites

##### OSX

Necessary libraries (`libusb`, `hidapi`) could be installed via [Homebrew](http://brew.sh/):

	brew install libusb hidapi

##### Linux (including Raspberry Pi)

`libusb` could be retrieved via `apt-get`

	sudo apt-get install libusb-1.0-0-dev libudev-dev

If the script is not intended to be started under `root`, proper permissions for the device should be set. Put the following two lines into a file `/etc/udev/rules.d/98-co2mon.rules`:

	KERNEL=="hidraw*", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="plugdev", MODE="0666"
	SUBSYSTEM=="usb", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="a052", GROUP="plugdev", MODE="0666"

and run `sudo udevadm control --reload-rules && udevadm trigger`.

###### Windows
For installation of `hidapi` package [Microsoft Visual C++ Compiler for Python](https://www.microsoft.com/en-us/download/details.aspx?id=44266) is required.

### Installation of python package

Then installation of `offgas` could be done via the `pip` utility:

	pip install hidapi offgas

[pandas package](http://pandas.pydata.org/) is required for use

**Note 1**: there could be a potential name conflict with the library `hid`. In this case the import of the module in python will fail with the error `AttributeError: 'module' object has no attribute 'windll'` (see [here](https://github.com/vfilimonov/co2meter/issues/1)). If this happens, please try uninstalling `hid` module (executing `pip uninstall hid` in the console).

**Note 2**: there were reports on issues with installation on Raspbian Stretch Lite (#5), where build failed with and `error code 1` in `gcc`. Most likely the reason is in missing dependencies. Possible solution is [described in the comment](https://github.com/vfilimonov/co2meter/issues/5#issuecomment-407378515).

# General usage

### Basic use

# Notes

* The output from the device is encrypted. I've found no description of the algorithm, except some GitHub libraries with almost identical implementation of decoding: [dmage/co2mon](https://github.com/dmage/co2mon/blob/master/libco2mon/src/co2mon.c), [maizy/ambient7](https://github.com/maizy/ambient7/blob/master/mt8057-agent/src/main/scala/ru/maizy/ambient7/mt8057agent/MessageDecoder.scala), [Lokis92/h1](https://github.com/Lokis92/h1/blob/master/co2java/src/Co2mon.java). This code is based on the repos above (method `CO2monitor._decrypt()`).
* The web-server does not do caching (yet) and was not tested (yet) over a long period of up-time.
* The whole setup is a bit heavy for such simple problem and (in case someone has time) could be simplified: e.g. talking to the device (in linux) could be done via reading/writing to `/dev/hidraw*`, parsing of the CSV and transformations could be done without `pandas`.


# Resources

Useful websites:
* [CO2meter]('http://github.com/vfilimonov/co2meter') the original co2meter script this one is based on
* [CO2MeterHacking](https://revspace.nl/CO2MeterHacking) with brief description of the protocol
* [ZG01 CO2 Module manual](https://revspace.nl/images/2/2e/ZyAura_CO2_Monitor_Carbon_Dioxide_ZG01_Module_english_manual-1.pdf) (PDF)
* [USB Communication Protocol](http://www.co2meters.com/Documentation/AppNotes/AN135-CO2mini-usb-protocol.pdf) (PDF)
* Habrahabr.ru blog-posts with the description, review and tests of the device: [part 1](http://habrahabr.ru/company/masterkit/blog/248405/), [part 2](http://habrahabr.ru/company/masterkit/blog/248401/), [part 3](http://habrahabr.ru/company/masterkit/blog/248403/) (Russian, 3 parts)

Scientific and commercial infographics:


# License
