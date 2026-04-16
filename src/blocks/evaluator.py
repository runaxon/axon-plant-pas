from myelin import Evaluator

class MyEvaluator(Evaluator):
    def score(self, measurements, scenario):
        """
        Compute loss for a single simulation run.

        Parameters
        ----------
        measurements: list of floats — one per timestep
        scenario: dict — simulation settings (dt, duration, target, state0)

        Returns
        -------
        float — loss for this patient/run (lower is better)
        """
        ise = 0.0
        induced = False
        dt = scenario['dt']
        for x in range(measurements):

    def aggregate(self, losses):
        """
        Combine per-patient losses into a single job-level scalar.
        Called in Python (not transpiled). losses: list of floats.
        """
        return 1.0 / len(losses) * losses ** 2.0
