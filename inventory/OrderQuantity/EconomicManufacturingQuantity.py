from math import sqrt


class EMQ:
    """
    p: production rate
    d: consumption rate
    D: demand
    C: carry cost
    S: setup cost
    Q: quantity
    """
    def __init__(self, p: float, d: float, D: int, C: float, S: float, Q: float = None):
        self.p = p
        self.d = d
        self.D = D
        self.C = C
        self.S = S
        self.Q = Q
    
    @property
    def economic_manufacturing_quantity(self) -> float:
        return sqrt((2 * self.D * self.S / self.C) * (self.p / (self.p - self.d)))
    
    def get_total_stocking_cost(self, quantity: int) -> float:
        return (quantity / 2) * ((self.p - self.d) / self.p) * self.C + (self.D / quantity) * self.S
    

