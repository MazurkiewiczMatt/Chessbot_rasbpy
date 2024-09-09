class ButtonSensors:
    def __init__(self, dummy=False):
        self.dummy = dummy
        pins = [14, 15, 18, 23, 24, 25, 8, 7]
        pull_up_pins = [14, 18, 23, 24, 25, 8, 7]  # excluded 15 due to faulty electronics
        if not dummy:
            from gpiozero import Button
            self.buttons = [Button(pin, pull_up=(pin in pull_up_pins)) for pin in pins]

    def sense(self):
        if self.dummy:
            return [False] * len(self.pins)
        else:
            return [button.is_pressed for button in self.buttons]
