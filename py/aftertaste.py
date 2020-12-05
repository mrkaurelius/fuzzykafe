import numpy as np
import matplotlib.pyplot as plt
from fuzzylab import trimf


class Membership():
    name = "" # DUSUK, ORTA, YUKSEK
    interval_start = None
    interval_end = None 
    x = None
    y = None
    
    def build_arrays(self):
        x = np.linspace(6.5, 8.5, 101)
        y = trimf(x, [7, 7.5, 8])
    
    def calc_membership(self, x):
        # find indice of x and return y[ind]
        return 0
    
    def __init__(self, name, i_start, i_end):
        self.name = name
        self.interval_start = i_start
        self.interval_end = i_end
        

class AfterTaste():
    memberships = []
    
    def calc_memberships(self, x):
        for m in self.memberships:
            if x >= m.interval_start or x <= m.interval_end:
                m.value = ()
        
    # def calc_meber
    def __init__():
        pass
    

# x = np.linspace(6.5, 8.5, 101)
# y = trimf(x, [7, 7.5, 8])
# for i in range(len(x)):
#     print(x[i], y[i])

# plt.plot(x, y)
# plt.xlabel('trimf, P = [3, 6, 8]')
# plt.show()