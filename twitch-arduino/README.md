# Twitch notification system for Arduino

This Python script takes the specified Twitch user's followed channels, and notifies the user through an LCD screen connected to an Arduino if a channel goes live.

Before running the script, make sure to fill in the required fields on the top of the twitch-arduino.py file:
* **CLIENT_ID** *string* The client ID for your application. You can get one [here](https://dev.twitch.tv/dashboard/apps/create).
* **OAUTH_ID** *string* Your OAuth token.
* **USER_ID** *string* Your Twitch account's user ID.
* **SERIAL_PORT** *string* The serial port the Arduino is connected to.
* **BAUD_RATE** *integer* Baud rate of the serial communication for the Arduino.
* **TIMEOUT** *integer* Timeout value for the serial port.
* **INTERVAL** *integer* Check interval in seconds.

## Hardware
* Arduino Mega 2560
* 16x2 LCD Display based on the Hitachi HD44780 driver

Wiring and sample code can be found [here](https://www.arduino.cc/en/Tutorial/LiquidCrystalDisplay).
#### Additional notes
* Two pushbuttons connected to pins 22 and 23 in pullup mode
* Pin 15 (backlight anode) of the LCD connected to pin 8 through a 320 ohm resistor

## Arduino libraries
* Built-in LCD library
* [Bounce2](https://github.com/thomasfredericks/Bounce2)

## Python dependencies
* [pyserial](https://github.com/pyserial/pyserial)
* [python-twitch-client](https://github.com/tsifrer/python-twitch-client)

### Disclaimer
This is my first real Python project, and as such the code is probably horribly inefficient. Any suggestions, feedback and questions are welcome and appreciated.
