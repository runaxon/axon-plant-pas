from myelin import Controller

class MyController(Controller):

    def __init__(self, kp, ki, kd, setpoint, remi_rate):
        self.first_reading = True
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.prev_measurement = -1
        self.remi_rate = remi_rate

    def configure(self, dt):
        self.dt = dt

    def step(self, measurement):
        # BIS > setpoint means deliver more
        error = measurement - self.setpoint
        p = self.kp * error
        self.integral += error * self.dt
        i = self.ki * self.integral
        if self.first_reading:
            d = 0
            self.first_reading = True
        else:
            d = self.kd * (measurement - self.prev_measurement) / self.dt
        u_propofol = p + i + d  # roll credits
        self.prev_measurement = measurement
        return u_propofol, self.remi_rate

    def reset(self):
        self.first_reading = True
        self.integral = 0.0
        self.prev_measurement = 0.0
