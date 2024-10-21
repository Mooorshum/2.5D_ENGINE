from math import sin, pi

class Wind:
    def __init__(self):
        self.t = 0
        self.dt = 0.1
        self.amplitudes = [0]
        self.frequencies = [0]

    def update(self):
        self.t += self.dt

    def get_wind_force(self):
        wind_force = 0
        for amplitude, frequency in zip(self.amplitudes, self.frequencies):
            wind_force += amplitude * sin(2 * pi * frequency * self.t)
        return wind_force
