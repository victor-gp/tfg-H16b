class DynamicalSystem:

    def __init__(self, a1, b1, c1, alpha1, beta1, a2, b2, c2, alpha2, beta2):
        self.a1 = a1
        self.b1 = b1
        self.c1 = c1
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.a2 = a2
        self.b2 = b2
        self.c2 = c2
        self.alpha2 = alpha2
        self.beta2 = beta2


    def eval(self, point, t):
        [x, y] = point
        x2 = x*x
        xy = x*y
        y2 = y*y

        dxdt = self.a1*x2 + self.b1*xy + self.c1*y2 + self.alpha1*x + self.beta1*y
        dydt = self.a2*x2 + self.b2*xy + self.c2*y2 + self.alpha2*x + self.beta2*y

        return [dxdt, dydt]
