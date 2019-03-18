class Led:
    def __init__(self, led_id):
        self.led_id = led_id

    def on(self):
        print(f'turn on {self.led_id}')

    def off(self):
        print(f'turn off {self.led_id}')

    def blink(self, on, freq):
        print(f'blink led {self.led_id} with freq {freq} Hz at {on} %')
