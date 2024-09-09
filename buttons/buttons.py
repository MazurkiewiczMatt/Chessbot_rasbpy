class ButtonSensors:
    def __init__(self, pins, dummy=False):
        self.dummy = dummy
        self.pins = pins
        if not dummy:
            from gpiozero import Button
            self.buttons = [Button(pin, pull_up=True) for pin in pins]

    def sense(self):
        if self.dummy:
            return [False] * len(self.pins)
        else:
            return [button.is_pressed for button in self.buttons]
