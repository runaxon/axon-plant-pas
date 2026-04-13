from myelin import Plant

class MyPlant(Plant):
    state_size  = ...  # number of state variables (int)
    input_size  = ...  # number of control inputs (int)
    params_size = ...  # number of model parameters (int)

    def derivatives(self, state, inputs, params):
        """
        ODE right-hand side.

        Parameters
        ----------
        state: tuple of floats — current state
        inputs: tuple of floats — control inputs
        params: tuple of floats — model parameters

        Returns
        -------
        tuple of floats — time derivatives of state
        """
        # x, = state          # example: single state
        # u, = inputs         # example: single input
        # k, = params         # example: single param

        # dx_dt = ...

        # return (dx_dt,)
        raise NotImplementedError
