from math import hypot, cos, sin, degrees, atan2, radians, pi, sqrt
import numpy as np

class Stanley_Method:
    def __init__(self, state, global_path, local_path):
        self.k = -0.8 # CTR parameter
        
        self.state = state
        self.global_path = global_path
        self.local_path = local_path
        self.yaw = []
        self.checkpoint = False # after parking, checkpoint is true

    def normalize(self, angle):
        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle
    
    def make_yaw(self):
        for i in range(len(self.global_path.x)-1):
            self.yaw.append(atan2(self.global_path.y[i+1]-self.global_path.y[i],\
                self.global_path.x[i+1]-self.global_path.x[i]))
        # print(self.yaw)  

    def run(self):
        if len(self.yaw) == 0:
            self.make_yaw()

        if self.state.mode == "local path tracking":
            path = self.local_path
        else:
            path = self.global_path

        front_x = self.state.x 
        front_y = self.state.y
    
        min_index = self.state.index

        map_x =  self.global_path.x[min_index]
        map_y =  self.global_path.y[min_index]
        map_yaw = self.yaw[min_index]
        dx = map_x - front_x
        dy = map_y - front_y
    

        perp_vec = [cos(radians(self.state.heading)+pi/2), sin(radians(self.state.heading)+pi/2)]
        cte = np.dot([dx, dy], perp_vec)
        
        if self.state.mode != "driving":
            k_s = 3.0 # must change
        else :
            k_s = 0
        k_s = 0

        final_yaw = -(map_yaw - radians(self.state.heading))
        # control law
        yaw_term = self.normalize(final_yaw)
        # cte_term = atan2(self.k*cte, self.state.speed)
        cte_term = atan2(self.k*cte,self.state.speed + k_s)

        direction = 1
        # steering
        if self.state.mode == "backward":
            direction = -1
        steer = degrees(yaw_term + cte_term)
        print(f"self.state.heading : {self.state.heading}")
        print(f"yaw_term : {degrees(yaw_term)}")
        print(f"cte_term : {degrees(cte_term)}")
        print(f"-----index : {min_index}")

        return max(min((steer)*direction, 27.0), -27.0)
        # return real_steer
        # return steer