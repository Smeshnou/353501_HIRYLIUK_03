import statistics

class Taylor:
    def __init__(self, x = 0., eps = 0.1):
        self.x = x
        self.eps = eps
        self.list = []
        sum = 0.
        for n in range(1, 501):
            step = pow(-1, n - 1) * pow(x, n) / n
            self.list.append(step)
            sum += step
            if abs(step) < eps :
                break
        self.f = sum
        self.n = n
        
    @property
    def list_mean(self):
        return statistics.mean(self.list)
    
    @property
    def list_median(self):
        return statistics.median(self.list)
    
    @property
    def list_mode(self):
        return statistics.mode(self.list)
    
    @property
    def list_variance(self):
        return statistics.variance(self.list)
    
    @property
    def list_stdev(self):
        return statistics.stdev(self.list)
    
    def __str__(self):
        return "x: {}, y: {}, n: {}, eps: {}, mean: {}, median: {}, mode: {}, variance: {}, stdev: {}".format(self.x, self.f, self.n, self.eps, self.list_mean, self.list_median, self.list_mode, self.list_variance, self.list_stdev)