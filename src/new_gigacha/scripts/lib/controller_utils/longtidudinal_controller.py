
from lib.controller_utils.pid import PID
from copy import copy
class longitudinalController:
    
    def __init__(self, state):
        self.state = state
        self.accel = PID(5, 0.5, 1)
        self.decel = PID(1, 1, 1) #TODO ABS? instead of PID


    def run(self):
        if self.state.target_speed == 0.0:
            return 0, self.decel.run() #speed, brake
        else:
            return self.accel.run(self.state.speed, self.state.target_speed), 0 #speed, brake