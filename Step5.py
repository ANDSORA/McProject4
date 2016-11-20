import serial
import time
import sys
from evaluator import evaluator


myeval = evaluator()

s = serial.Serial('/dev/ttyACM1', 115200, timeout=1)  # opens a serial port (resets the device!)
time.sleep(2)  # give the device some time to startup (2 seconds)

# write to the device’s serial port
s.write(b"a[AB]\n")  # set the device address to AB
time.sleep(0.1)  # wait for settings to be applied
# print(s.readline())

s.write(b"c[1,0,5]\n")  # set number of retransmissions to 5
time.sleep(0.1)  # wait for settings to be applied
# print(s.readline().decode('unicode_escape').strip())

s.write(b"c[0,1,30]\n")  # set FEC threshold to 30 (apply FEC to packets with payload >= 30)
time.sleep(0.1)  # wait for settings to be applied

message = "\0"
payload = 1
s.write(("m["+message+",CD]\n").encode("ascii"))

"""
while True:
    print(s.readline().decode('unicode_escape').strip())
"""

mycount = 0
# set the loop for transmission
while mycount <= 20:
    # driven by serial.readline()
    received = s.readline().decode('unicode_escape').strip()
    if len(received) > 0:
        print(received)
        # distinguish the message we get
        event_type = received[0]
        content = received[2:-1]
        if event_type == 'm' and content == "D": # it is a ATK
            s.write(("m["+message+",CD]\n").encode("ascii"))
            time.sleep(2.0)
            mycount += 1
        elif event_type == "s": # it is a statistic message and should be handled
            print(mycount)
            myeval.update(content)
            
myeval.writeToFile()


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
