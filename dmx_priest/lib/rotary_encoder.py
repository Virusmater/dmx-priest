from gpiozero import Button


class RotaryEncoder:

    LEFT = -1
    RIGHT = 1
    BUTTON = 0

    def __init__(self, callback):
        self.pin_a = Button(18)  # Rotary encoder pin A connected to GPIO2
        self.pin_b = Button(27)  # Rotary encoder pin B connected to GPIO3
        self.sw = Button(17)
        self.pin_a.when_pressed = self.pin_a_rising  # Register the event handler for pin A
        self.pin_b.when_pressed = self.pin_b_rising  # Register the event handler for pin B
        self.sw.when_pressed = self.pin_sw_rising
        self.callback = callback

    def pin_a_rising(self):  # Pin A event handler
        if self.pin_b.is_pressed:
            self.callback(RotaryEncoder.LEFT)  # pin A rising while A is active is a clockwise turn

    def pin_b_rising(self):  # Pin B event handler
        if self.pin_a.is_pressed:
            self.callback(RotaryEncoder.RIGHT)  # pin B rising while A is active is a clockwise turn

    def pin_sw_rising(self):
        if self.sw.is_pressed:
            self.callback(RotaryEncoder.BUTTON)
