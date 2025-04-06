from trajectory import *

class RobotArmHandler:
    def __init__(self):
        self.scheduled_movements = []
        self.command_queue = []
        self.current_command_index = 0
        self.can_move = True  # Assume can move initially; adjust based on Arduino feedback
        self.position = [0, 0]  # Assuming starting position at (0,0)
        self.discard_positions = [(8, 3), (8, 4)]
        self.current_discard_index = 0
        self.raising_height = 15  # Example raising height
        self.discard_height = 5  # Example discard height
        self.matrixHeights = [
            [0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 2],
            [0, 0, 0, 0, 1, 1, 2, 2],
            [0, 0, 0, 0, 1, 1, 2, 2],
            [0, 0, 0, 0, 0, 1, 1, 2],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ]

    def schedule_movement(self, movement_params):
        self.scheduled_movements.append(movement_params)
        if not self.command_queue:
            self._process_next_movement()

    def _process_next_movement(self):
        if self.scheduled_movements:
            movement = self.scheduled_movements.pop(0)
            self.command_queue = self._analyze_move(movement)
            self.current_command_index = 0

    def _analyze_move(self, movement):
        start, end = movement
        commands = []
        start_rank, start_file = start
        end_rank, end_file = end

        # Check if end position is occupied (capture)
        if self.matrixHeights[end_rank][end_file] > 0:
            # Capture sequence
            # Move to end to pick up captured piece
            commands.extend(self._generate_move_commands(self.position, end))
            # Lower EM to captured piece's height
            capture_height = self.matrixHeights[end_rank][end_file]
            commands.append(f"EM_D {capture_height}")
            commands.append("EM_ON")
            commands.append(f"EM_R {self.raising_height}")
            # Move to discard area
            discard_pos = self.discard_positions[self.current_discard_index]
            self.current_discard_index = (self.current_discard_index + 1) % len(self.discard_positions)
            commands.extend(self._generate_move_commands(end, discard_pos))
            # Drop in discard
            commands.append(f"EM_D {self.discard_height}")
            commands.append("EM_OFF")
            commands.append(f"EM_R {self.raising_height}")
            # Update position to discard area
            self.position = discard_pos

        # Move the piece from start to end
        # Move to start position
        commands.extend(self._generate_move_commands(self.position, start))
        # Pick up the piece
        start_height = self.matrixHeights[start_rank][start_file]
        commands.append(f"EM_D {start_height}")
        commands.append("EM_ON")
        commands.append(f"EM_R {self.raising_height}")
        # Move to end position
        commands.extend(self._generate_move_commands(start, end))
        # Place the piece
        place_height = self.matrixHeights[end_rank][end_file] if self.matrixHeights[end_rank][
                                                                     end_file] > 0 else start_height
        commands.append(f"EM_D {place_height}")
        commands.append("EM_OFF")
        commands.append(f"EM_R {self.raising_height}")
        # Update current position to end
        self.position = end

        return commands

    def _generate_move_commands(self, from_pos, to_pos):
        steps1, steps2 = self._calculate_stepper_steps(from_pos, to_pos)
        return [f"MOVE {steps1} {steps2}"]

    def _calculate_stepper_steps(self, from_pos, to_pos):
        x1, y1 = 15.75 - from_pos[0] * 4.5, 6.75 + from_pos[1] * 4.5
        x2, y2 = 15.75 - to_pos[0] * 4.5  , 6.75 + to_pos[1] * 4.5
        try:
            start_shoulder1, start_shoulder2 = trajectory.calc_angles(x1, y1)
            end_shoulder1, end_shoulder2 = trajectory.calc_angles(x2, y2)
        except:
            print("Unreachable position")
            return 0, 0

        # Calculate step difference
        steps1, steps2 = trajectory.calculate_step_difference(
            (start_shoulder1, start_shoulder2),
            (end_shoulder1, end_shoulder2)
        )
        return steps1, steps2

    def update(self):
        if not self.command_queue and self.scheduled_movements:
            self._process_next_movement()

        if self.command_queue and self.current_command_index < len(self.command_queue):
            command = self.command_queue[self.current_command_index]
            self.current_command_index += 1
            return command
        else:
            self.command_queue = []
            self.current_command_index = 0
            return ""

