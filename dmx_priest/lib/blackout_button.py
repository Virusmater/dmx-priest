from gpiozero import Button


class BlackoutButton:

    def __init__(self, callback):
        self.pin = Button(5, hold_time=1)  # Rotary encoder pin A connected to GPIO5
        self.pin.when_held = self.pin_rising  # Register the event handler for pin A
        self.callback = callback


    def pin_rising(self):  # Pin A event handler
        if self.pin.is_pressed:
           print("blackout button pressed 1")
           self.callback()
