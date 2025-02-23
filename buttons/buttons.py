class ButtonSensors:
    def __init__(self, dummy=False):
        self.dummy = dummy
        self.pins = [14, 15, 18, 23,  # Player 1/2 buttons
                    24, 25, 7, 8]     # UI buttons 1-4
        pull_down_pins = []
        if dummy:
            self.buttons = [False for pin in self.pins]
        else:
            from gpiozero import Button
            self.buttons = [Button(pin, pull_up=not (pin in pull_down_pins)) for pin in self.pins]


    def sense(self):
        if self.dummy:
            return self.buttons
        else:
            return [button.is_pressed for button in self.buttons]
