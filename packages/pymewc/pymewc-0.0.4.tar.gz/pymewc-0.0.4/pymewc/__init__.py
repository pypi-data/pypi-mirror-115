from os import error


def pymewc():
    import time

    print("Thanks for using pymewc to record any issue mail to gr8rithic@gmail.com")
    time.sleep(1)
    print('----------------------------------------------------------------------------------------------------')
    time.sleep(1)
    print("You can also get in touch with me on github link https://github.com/gr8rithic/")
    time.sleep(1)
    print('----------------------------------------------------------------------------------------------------')
    time.sleep(1)
    print('Get connected via LinkedIn https://www.linkedin.com/in/rithic-hariharan-8902b4199/')
    time.sleep(1)
    print('----------------------------------------------------------------------------------------------------')
    time.sleep(1)
    print('Visit my postfolio https://gr8rithic.github.io/')
    time.sleep(1)
    print('----------------------------------------------------------------------------------------------------')
    time.sleep(1)
    print()
    print("Setting up the environment")
    time.sleep(3)


    com_port = input("Enter the com-port(Com4 or /dev/ttyACM0 on Windows and Unix based respectively)")
    baud_rate = int(input("Enter the baud rate as specified in the .ino file"))
    import serial  #importing the package
    try:
        ser = serial.Serial(com_port, baud_rate)  #entering the port name and specifying the boad rate
    except error:
        print("Check the usb port is mentioned correctly or usb is connected properly")

    while(1):
        try:
            x = (ser.readline().strip())  #reading the serial print value
            y = (x.decode('utf-8'))       #decoding the output value
            print(y)                      #printing out the value

        except UnicodeDecodeError:
            continue                      #utf8 decoding issue

def hello():
    print("Hellow world")

