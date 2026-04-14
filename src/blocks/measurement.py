from myelin import Measurement

class MyMeasurement(Measurement):
    def measure(self, state, params):

      Ce_prop = state[3]
      Ce_remi = state[7]

      e0 = params[14]
      emax = params[15]
      c50_prop = params[16]
      c50_remi = params[17]
      gamma = params[18]

      # Bouillon interaction model
      U = (Ce_prop / c50_prop) + (Ce_remi / c50_remi)

      # BIS calc from U
      bis = e0 - emax * (U ** gamma) / (U ** gamma + 1.0)
      return bis
