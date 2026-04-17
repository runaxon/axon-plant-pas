from myelin import Evaluator

# Loss function parameters — match axon-plant-schnider exactly
BIS_TARGET = 50.0  # maintenance BIS target
T_INDUCTION = 2.0  # min — BIS must cross below 60 by this time
T_MAINTENANCE = 30.0  # min — end of maintenance window (washout excluded)
LAMBDA = 500_000.0
ISE_REF = BIS_TARGET ** 2 * (T_MAINTENANCE - T_INDUCTION)  # 70,000
LAMBDA_NORM = LAMBDA / ISE_REF  # ~7.14

class PASEvaluator(Evaluator):
    def score(self, measurements, scenario):
        """
        ISE over maintenance window + induction penalty if BIS never crosses 60
        within T_INDUCTION minutes. Normalized by ISE_REF so loss is in [0, ~1].
        """
        dt = scenario['dt']
        ise = 0.0
        induced = False
        t = 0.0

        for bis in measurements:
            if t <= T_INDUCTION and bis < 60.0:
                induced = True
            if T_INDUCTION <= t <= T_MAINTENANCE:
                ise += (bis - BIS_TARGET) ** 2 * dt
            t += dt

        induction_penalty = 0.0 if induced else LAMBDA_NORM
        return ise / ISE_REF + induction_penalty

    def aggregate(self, losses):
        return sum(losses) / len(losses)
