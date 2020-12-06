class Membership():
    name = "" # DUSUK, ORTA, YUKSEK
    interval_start = None
    interval_end = None 
    
    def __init__(self, name, i_start, i_end):
        self.name = name
        self.interval_start = i_start
        self.interval_end = i_end