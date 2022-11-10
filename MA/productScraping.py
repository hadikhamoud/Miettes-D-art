import keyboard
from time import sleep as sl


sl(5)

for i in range(30):
    sl(1)
    keyboard.press_and_release('tab')
    keyboard.press_and_release('tab')
    keyboard.press_and_release('tab')
    keyboard.press_and_release('enter')
    sl(2)

    keyboard.press_and_release('cmd+s')
    sl(1)

    keyboard.press_and_release('enter')
    sl(4)
    keyboard.press_and_release('cmd+[')

    
    
     
     
     

