import time
import random
from pynput.keyboard import Controller

keyboard = Controller()  # Create the controller


for i in range(100):
    keyboard.type('Warning: low battery\n')              # Type the character
    delay = 60 # random.uniform(0, 2)   # Generate a random number between 0 and 10
    time.sleep(delay)                   # Sleep for the amount of seconds generated
    print ('Elapsed: ' + str(i) + ' minutes')
