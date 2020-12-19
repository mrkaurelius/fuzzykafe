from math import ceil

class Membership():
    intv_size = 1001 # interval size for x axis
    x_start = 0
    x_end = 10
    
    def __init__(self, name, i_start, i_end):
        self.name = name # DUSUK, ORTA, YUKSEK
        self.i_start = i_start
        self.i_end = i_end                
        self.x = None
        self.y = None
        self.tri_list = None
    
    def set_arrays(self):
        # x = np.linspace(6.5, 8.5, 101)
        # y = trimf(x, [7, 7.5, 8])
        pass
    
    def calc_membership(self, x):
        # find indice of x and return y[ind]
        # 0 ile 10 arasinda gelen
        if x < 0 or x > 10:
            raise KeyError('membership value must be in (0, 10) interval.') 
       
        t = Membership.intv_size // Membership.x_end
        x_ind = ceil(t * x) # ceil number
        # print(t, x_ind)
        return self.y[x_ind]

    def __repr__(self):
        return repr(self.name + ', Start: ' + str(self.i_start) + ', End: ' + str(self.i_end))