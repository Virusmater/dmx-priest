from gpiozero import Button
import queue

eventq = queue.Queue()

pin_a = Button(18)  # Rotary encoder pin A connected to GPIO2
pin_b = Button(27)  # Rotary encoder pin B connected to GPIO3
sw = Button(17)

LEFT = -1
RIGHT = 1
BUTTON = 0


def pin_a_rising():  # Pin A event handler
    if pin_b.is_pressed:
        eventq.put(LEFT)  # pin A rising while A is active is a clockwise turn


def pin_b_rising():  # Pin B event handler
    if pin_a.is_pressed:
        eventq.put(RIGHT)  # pin B rising while A is active is a clockwise turn


def pin_sw_rising():
    if sw.is_pressed:
        eventq.put(BUTTON)


pin_a.when_pressed = pin_a_rising  # Register the event handler for pin A
pin_b.when_pressed = pin_b_rising  # Register the event handler for pin B
sw.when_pressed = pin_sw_rising

