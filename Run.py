import RPi.GPIO as gpio
import serial
import sys
import os
gpio.setwarnings(False)
print('\33[33m'+"for emergency turn off, press " +'\x1b[6;37;42m'+"ctrol+c"+'\x1b[0m')
print('\33[33m'+"or press any key on remote control "+'\x1b[0m')
arduino = serial.Serial("/dev/ttyACM0",250000)
gpio.setmode(gpio.BOARD)
gpio.setup(3,gpio.IN)



def IRtrigger(pin):
    print(' ')
    print('\33[31m'+"IR Sensor triggered!!  "+'\x1b[0m')
#    print('\33[31m'+"interrupted!  "+'\x1b[0m')
    print('\33[33m'+"shutting system down...  "+'\x1b[0m')
    gpio.output(12,False)
    print('\x1b[7;37;42m'+"X-RAYs OFF"+'\x1b[0m')
    arduino.write(b"M112\n")      #emergency stop
    print('\x1b[7;37;42m'+"Motors OFF"+'\x1b[0m')
    sys.exit()
    
    

gpio.add_event_detect(3,gpio.RISING, callback=IRtrigger, bouncetime=300)

try:
    import Main
                    
                    
except KeyboardInterrupt:
    print(' ')
    print('\33[31m'+"interrupted!  "+'\x1b[0m')
    print('\33[33m'+"shutting system down......  "+'\x1b[0m')
    gpio.output(12,False)
    print('\x1b[7;37;42m'+"X-RAYs OFF"+'\x1b[0m')
    arduino.write(b"M112\n")      #emergency stop
    print('\x1b[7;37;42m'+"Motors OFF"+'\x1b[0m')

    