import numpy as np


class ORLib:
    def __init__(self, name):
        with open(name + ".txt", "r") as file:
            self.n = int(file.readline().split()[0])
            self.mean_return = np.zeros(self.n)
            self.return_deviation = np.zeros(self.n)
            for i in range(self.n):
                line = file.readline().split()
                self.mean_return[i] = float(line[0])
                self.return_deviation[i] = float(line[1])
            self.sigma = np.zeros((self.n, self.n))
            for c in range(self.n ** 2):
                line = file.readline().split()
                if not line:
                    break
                self.sigma[int(line[0]) - 1, int(line[1]) - 1] = float(line[2])
                self.sigma[int(line[1]) - 1, int(line[0]) - 1] = float(line[2])
