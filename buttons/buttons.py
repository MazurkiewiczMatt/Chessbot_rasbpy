class ButtonSensors:
    def __init__(self, dummy=False):
        self.dummy = dummy
        pins = [14, 15, 18, 23, 24, 25, 8, 7]
        if not dummy:
            from gpiozero import Button
            self.buttons = [Button(pin, pull_up=True) for pin in pins]

    def sense(self):
        if self.dummy:
            return [False] * len(self.pins)
        else:
            return [button.is_pressed for button in self.buttons]
