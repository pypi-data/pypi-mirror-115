try:
    from gpiozero import Button
    from gpiozero import LED
    import time

    import sys, os, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)

    from define import *

    fan=LED(FAN_PWM_PIN, initial_value=True)

    def fanTurnOn(on):
        global fan
        if on:
            fan.off()
        else:
            fan.on()
    if __name__ == "__main__":
        fanTurnOn(True)
        time.sleep(5)
        fanTurnOn(False)
        time.sleep(5)
        fanTurnOn(True)
        time.sleep(5)
        fanTurnOn(False)
except Exception as e:
    print(e)
    pass
    
    
