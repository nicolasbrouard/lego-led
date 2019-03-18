import threading
from time import sleep

from led import Led


class ActionThread(threading.Thread):
    def __init__(self, led_id, delay, on, freq):
        super().__init__()
        self.freq = freq
        self.led_id = led_id
        self.on = on
        self.delay = delay

    def run(self):
        if self.delay != 0:
            sleep(self.delay)

        if self.on == 0:
            Led(self.led_id).off()
        elif self.on == 100:
            Led(self.led_id).on()
        else:
            Led(self.led_id).blink(self.on, self.freq)
