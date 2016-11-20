import serial
import time
import sys
from evaluator import evaluator


myeval = evaluator()

s = serial.Serial('/dev/tty.usbmodem1411', 115200, timeout=1)  # opens a serial port (resets the device!)
time.sleep(2)  # give the device some time to startup (2 seconds)

# write to the device’s serial port
s.write(b"a[CD]\n")  # set the device address to AB
time.sleep(0.1)  # wait for settings to be applied
# print(s.readline())

s.write(b"c[1,0,5]\n")  # set number of retransmissions to 5
time.sleep(0.1)  # wait for settings to be applied
# print(s.readline().decode('unicode_escape').strip())

s.write(b"c[0,1,30]\n")  # set FEC threshold to 30 (apply FEC to packets with payload >= 30)
time.sleep(0.1)  # wait for settings to be applied

message = "a"
s.write(("m["+message+",AB]\n").encode("ascii"))

while True:
    received = s.readline().decode('unicode_escape').strip()
    if len(received) > 0:
        event_type = received[0]
        content = received[2:-1]
        if event_type == 'm' and content == "D":
            s.write(("m["+message+",AB]\n").encode("ascii"))
        elif event_type == "s":
            myeval.update(content)

# read from the device’s serial port (should be done  in a separate thread)
# message = ""
# while True:  # while not terminated
#     try:
#         print(s.readline().decode('unicode_escape').strip())
#
#         # byte = s.read(1).decode('ascii')  # read one byte (blocks until data available or timeout reached)
#         # if byte == '\n':  # if termination character reached
#         #     print(message)  # print message
#         #     message = ""  # reset message
#         # else:
#         #     message = message + byte  # concatenate the message
#     except serial.SerialException:
#         continue  # on timeout try to read again
#     except KeyboardInterrupt:
#         sys.exit()  # on ctrl-c terminate program
