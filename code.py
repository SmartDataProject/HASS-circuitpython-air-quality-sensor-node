import board
import busio
from busio import I2C
from digitalio import DigitalInOut, Direction
#from ujson import dumps

try:
    import struct
except ImportError:
    import ustruct as struct

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Main  loop reads from PMS sensor
# Connect the Sensor's TX pin to the board's RX pin
uart = busio.UART(board.TX, board.RX, baudrate=9600)
buffer = []

while True:
    try:
        data = uart.read(32)  # read up to 32 bytes
        data = list(data)
        buffer += data
    except:
        continue

    while buffer and buffer[0] != 0x42:
        buffer.pop(0)

    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue

    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue

    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue

    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame

    check = sum(buffer[0:30])

    if check != checksum:
        buffer = []
        continue

    data_dict = {}
    data_dict['particles_03um'] = particles_03um
    data_dict['particles_05um'] = particles_05um
    data_dict['particles_10um'] = particles_10um
    data_dict['particles_25um'] = particles_25um
    data_dict['particles_50um'] = particles_50um
    data_dict['particles_100um'] = particles_100um
    #print(data_dict)
    # print(tuple(data_dict.values())) # for mu plotting
    
    # print json string without json.dumps
    data_string = """ "a": {a}, "b": {b}, "c": {c}, "d": {d}, "e": {e}, "f": {f} """.format(
            a=particles_03um,
            b=particles_05um,
            c=particles_10um,
            d=particles_25um,
            e=particles_50um,
            f=particles_100um
            )

    print(""" {""" + data_string + """ } """)
    
    

    buffer = buffer[32:]
    # print("Buffer ", buffer)