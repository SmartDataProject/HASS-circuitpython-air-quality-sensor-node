# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with various air quality sensors, powered over serial (USB) and piping data into Home-Assistant using json strings. Note that Home-Assitant is merely a consumer of the sensor data, and alternatively the data could be plotted in a Jupyter notebook, as [here](https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb).

I am running Home-Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep complex data parsing logic in python on the board. In Home-Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML. I previously used this approach with a BBC microbit [here](https://github.com/robmarkcole/HASS-BBC-envirobit).

## Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython Bundle library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded (this project assumes you have done this). It has both 3.3 and 5V output, and all the connections are clearly labelled. The board shows up as an external USB drive, making it straightforward to update the code on the board. Don't forget to [update the firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3, a process which simply involves dragging a `.uf2` file onto the board. Copy `code.py` from this repository onto the board, and wire up the sensor as described in the next section.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="800">
</p>

## PMS5003 laser air sensor
This sensor and accompanying Circuitpython code is on the Adafruit website [here](https://learn.adafruit.com/pm25-air-quality-sensor). For more links see [here](https://github.com/OxygenLithium/Pollutant-Mapping). The wiring between the PMS (by cable colour) and the Metro M0 board are given in the table below. Note that the RX (receive line) of the PMS is wired to the TX (transmit line) of the Metro, and vice versa, to enable comms.

| PMS (cable) |  Metro M0 |
|:-----------:|:---------:|
| 5V (purple) | 5V output |
| 0V (orange) |    GND    |
|  RX (blue)  |   1 (TX)  |
|  TX (green) |   0 (RX)  |

## MU
For development I recommend [MU](https://codewith.mu/), which is a user friendly QT5 GUI which allows programming with the circuitpython/micropython, just `pip install mu-editor` and run with `mu-editor`. It also allows [live plotting of data](https://codewith.mu/en/tutorials/1.0/plotter) just by printing a tuple of data. Github source [here](https://github.com/mu-editor/mu), and for further inspiration see https://madewith.mu/.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/mu.png" width="1000">
</p>

## Home-Asasistant
We integrate the board via a [serial sensor](https://www.home-assistant.io/components/sensor.serial/) and breakout the individual readings using [template sensors](https://www.home-assistant.io/components/sensor.template/):
```yaml
sensor:
  - platform: serial
    serial_port: /dev/tty.usbmodem141401
  - platform: template
    sensors:
      particles_03um:
        friendly_name: particles_03um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.a }}"
  - platform: template
    sensors:
      particles_05um:
        friendly_name: particles_05um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.b }}"
  - platform: template
    sensors:
      particles_10um:
        friendly_name: particles_10um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.c }}"
  - platform: template
    sensors:
      particles_25um:
        friendly_name: particles_25um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.d }}"
  - platform: template
    sensors:
      particles_50um:
        friendly_name: particles_50um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.e }}"
  - platform: template
    sensors:
      particles_100um:
        friendly_name: particles_100um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.f }}"

history_graph:
  pms5003:
    entities:
      - sensor.particles_03um
      - sensor.particles_05um
      - sensor.particles_10um
      - sensor.particles_25um
      - sensor.particles_50um
      - sensor.particles_100um
```

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/ha.png" width="550">
</p>

## Display
I wish to add a display, perhaps https://thepihut.com/collections/lcds-displays/products/adafruit-1-54-tri-color-eink-epaper-display-with-sram-ada3625

## Streaming data in Jupyter
For streaming see http://pyviz.org/tutorial/11_Streaming_Data.html

## VS-code
Developing Circuitpython in [MS VS-code](https://code.visualstudio.com/) is quite a nice experience, although not as seamless as using Mu. For instance, I found my terminal often froze between restarts of the board, which wasn't an issue with Mu. I have the [pycom VS code extension installed](https://docs.pycom.io/pymakr/installation/vscode) which adds a terminal. I use the terminal to connect to the board using `screen`. First check which port the board is on with `ls /dev/tty.*` then connect to the board with e.g. `screen /dev/tty.usbmodem141401`. As the board shows up as a USB device you can drag the `code.py` file into VS-code and edit. On hitting `save` the board restarts and the edits are immediately implemented.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/vs_code.png" width="1000">
</p>

## Presentation
See a presentation on this project at https://gitpitch.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/master

## Links
* [Awesome Circuitpython](https://github.com/adafruit/awesome-circuitpython)
* https://www.adafruit.com/circuitpython
