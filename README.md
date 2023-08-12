# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/volume-mute.svg' card_color='#022B4F' width='50' height='50' style='vertical-align:bottom'/> Pushbutton speak/stop skill

## About
This Mycroft skill is written assuming that there is a pushbutton and an LED connected to a Raspberry Pi. 

A long press of the button is the same as speaking the wake word, allowing the user to then speak a command. A short press is the same as giving the 'stop' command and hence will stop the playback of any audio.

The LED lights up whenever audio is being played (through the audioservice).

The GPIO pins that the button and LED are connected to and the polarity of the signals are configurable via the settings.

## Important
This skill is made for Picroft Lightning, which is Picroft on Rasbian Stretch.

## Category
**IoT**

## Credits
Simon Waller

## Supported Devices
platform_picroft

## Tags
media
tools
