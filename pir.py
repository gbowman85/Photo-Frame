
#!/usr/bin/env python

import sys
import time
import RPi.GPIO as io
import subprocess

io.setmode(io.BCM)
SHUTOFF_DELAY = 10 # seconds
SWITCHON_DELAY = 3 # seconds
PIR_PIN = 25       # 22 on the board
LED_PIN = 16

def main():
    io.setup(PIR_PIN, io.IN)
    #io.setup(LED_PIN, io.OUT)
    turned_off = False
    last_motion_time = time.time()
    last_still_time = time.time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            #io.output(LED_PIN, io.LOW)
            #print ".",
            sys.stdout.flush()
            if turned_off and time.time() > (last_still_time + SWITCHON_DELAY):
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turn_off()
            #print "x"
            last_still_time = time.time()
            #if not turned_off and time.time() > (last_motion_time + 1):
            #    io.output(LED_PIN, io.HIGH)
        time.sleep(1)

def turn_on():
    subprocess.call("sh /usr/local/bin/monitor_on.sh", shell=True)

def turn_off():
    subprocess.call("sh /usr/local/bin/monitor_off.sh", shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()


