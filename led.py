class Led:
    def __init__(self, led_id):
        self.led_id = led_id

    def on(self):
        print('turn on {self.led_id}')

    def off(self):
        print('turn off {self.led_id}')

    def blink(self, on, freq):
        print('blink led {self.led_id} with freq {freq} Hz at {on} %')
