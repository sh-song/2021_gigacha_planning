
from math import hypot
class IndexFinder:
    def __init__(self, ego):
        self.ego = ego

    def run(self):
        min_dis = -1
        min_idx = 0
        print(len(self.ego.global_path.x))
        for i in range(max(self.ego.index - 3, 0), self.ego.index + 3):
            dis = hypot(self.ego.global_path.x[i] - self.ego.pose.x, self.ego.global_path.y[i] - self.ego.pose.y)
            if min_dis > dis or min_dis == -1:
                min_dis = dis
                min_idx = i
        self.ego.index = min_idx
