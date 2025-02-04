class RobotArmHandler:
    def __init__(self):
        self.scheduled_movements = []
        self.can_move = False

    def schedule_movement(self, movement_params):
        self.scheduled_movements.append(movement_params)

    def update(self):
        arduino_instruction = ""
        # check with arduino whether it can move again
        if False:
            self.can_move = True

        if self.can_move and self.schedule_movements != []:
            self.can_move = False
            arduino_instruction = ""

        return arduino_instruction

