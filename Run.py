import RPi.GPIO as gpio
import serial
gpio.setwarnings(False)
print('\33[33m'+"for emergency turn off, press " +'\x1b[6;37;42m'+"ctrol+c"+'\x1b[0m')

arduino = serial.Serial("/dev/ttyACM0",250000) 


try:
    import Main
                    
                    
except KeyboardInterrupt:
    print('\33[31m'+"interrupted!  "+'\x1b[0m')
    print('\33[33m'+"implementing system turn off...  "+'\x1b[0m')
    gpio.output(12,False)
    print('\x1b[7;37;42m'+"X-RAYs OFF"+'\x1b[0m')
    arduino.write(b"M112\n")      #emergency stop
    print('\x1b[7;37;42m'+"Motors OFF"+'\x1b[0m')
