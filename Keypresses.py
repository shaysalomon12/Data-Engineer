import time
import random
from pynput.keyboard import Controller
from datetime import datetime

keyboard = Controller()  # Create the controller

print ('Started at ' + datetime.now().strftime("%H:%M:%S"))

for i in range(120):
    keyboard.type(' ')                  # Type the character
    delay = 60 # random.uniform(0, 2)   # Generate a random number between 0 and 10
    time.sleep(delay)                   # Sleep for the amount of seconds generated
    print ('Elapsed: ' + str(i+1) + ' minutes')

#---------1---------2---------3---------4---------5---------6---------7---------8---------9--------10--------11--------12 
#123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
# Put cursor at the beginning of the line above and click 'Play'