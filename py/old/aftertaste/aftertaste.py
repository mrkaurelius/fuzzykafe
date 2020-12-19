import numpy as np
import matplotlib.pyplot as plt

from fuzzylab import trimf
from .membership import Membership

class AfterTaste():
    # def calc_meber
    def __init__(self):
        self.memberships = []
    
    # return array of memberships
    def calc_memberships(self, x):
        ret = []
        for ms in self.memberships:
            ret.append(ms.calc_membership(x))
        return ret
    
    def build_memberships(self):
        dusuk_ms = Membership("DUSUK", 0, 7.5)
        orta_ms = Membership("ORTA", 7, 8)
        yuksek_ms = Membership("YUKSEK", 7.5, 10)
        #%% Dusuk
        # parametrik yap
        dusuk_ms.x = np.linspace(Membership.x_start, Membership.x_end, Membership.intv_size)
        dusuk_ms.tri_list = [6.5, 7, 7.5]
        dusuk_ms.y = trimf(dusuk_ms.x, dusuk_ms.tri_list)        
        for i in range(700):
            dusuk_ms.y[i] = 1
        # add membership
        self.memberships.append(dusuk_ms)
        #%% Orta        
        # parametrik yap
        orta_ms.x = np.linspace(Membership.x_start, Membership.x_end, Membership.intv_size)
        orta_ms.tri_list = [7, 7.5, 8]
        orta_ms.y = trimf(orta_ms.x, orta_ms.tri_list)
        self.memberships.append(orta_ms)        
        #%% Yuksek
        # parametrik yap
        yuksek_ms.x = np.linspace(Membership.x_start, Membership.x_end, Membership.intv_size)
        yuksek_ms.y = trimf(yuksek_ms.x, [7.5, 8, 10])
        for i in range(800,1001):
            yuksek_ms.y[i] = 1
        self.memberships.append(yuksek_ms)
    
    def plot(self):
        for i in range(len(self.memberships)):
            plt.plot(self.memberships[i].x, self.memberships[i].y)
        plt.show()