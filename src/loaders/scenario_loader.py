from myelin import ScenarioLoader
import json

class MyScenarioLoader(ScenarioLoader):

    default_id = 'default'

    def load(self, scenario_id):
        """
        Return scenario dict for the given scenario ID.

        Returns
        -------
        dict with at minimum:
            dt: float — timestep in simulation time units
            duration: float — total simulation duration
            target: float — controller setpoint
            state0: tuple of floats — initial plant state
        """
        with open(f'scenarios/{scenario_id}.json') as f:
            data = json.load(f)
        return {
            'dt': data['dt'],
            'duration': data['duration'],
            'target': data['target'],
            'state0': tuple(data['state0'])
        }
