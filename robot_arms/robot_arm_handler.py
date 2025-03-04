

class RobotArmHandler:
    def __init__(self):
        self.scheduled_movements = []
        self.can_move = False
        self.position=[[2,2],[2,5]]
        #1 zone, 2 underline area
        self.matrixZone=[[0,0,0,0,0,0,1,1],
                        [0,0,0,0,0,1,1,1],
                        [0,0,0,0,0,1,1,2],
                        [0,0,0,0,1,1,2,2],
                        [0,0,0,0,1,1,2,2],
                        [0,0,0,0,0,1,1,2],
                        [0,0,0,0,0,1,1,1],
                        [0,0,0,0,0,0,1,1]]

    def schedule_movement(self, movement_params):
        self.scheduled_movements.append(movement_params)
    def is_in_zone(self,startMove):
        if self.matrixZone[startMove[0]][startMove[1]] == 1:
            return True
        else:
            return False
    def is_under_line(self,coordinates):
        if self.matrixZone[coordinates[0]][coordinates[1]] > 0:
            return True
        else:
            return False
    def analyse_coordinates(self,two_coordinates):
        start_position=two_coordinates[0]
        end_position=two_coordinates[1]
        start_position_is_under=self.is_under_line(start_position)
        end_position_is_under=self.is_under_line(end_position)
        start_position_is_in_zone=self.is_in_zone(start_position)
        return start_position_is_under, end_position_is_under, start_position_is_in_zone

    #def
    def update(self):
        arduino_instruction = ""
        # check with arduino whether it can move again
        if False:
            self.can_move = True

        if self.can_move and self.schedule_movements != []:
            self.can_move = False
            arduino_instruction = ""

        return arduino_instruction

