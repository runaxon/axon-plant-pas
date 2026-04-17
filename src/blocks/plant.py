from myelin import Plant

class MyPlant(Plant):

    state_size = 8  # 4 for propofol and 4 for remifentanil
    input_size = 2  # propofol and remifentanil
    params_size = 19  # 7 for propofol and 7 for remifentanil 

    def derivatives(self, state, inputs, params):
        
        # Unpackage inputs
        u_prop, u_remi = inputs[0:2]

        # Unpackage propofol compartments
        x1_prop, x2_prop, x3_prop, Ce_prop = state[0:4]

        # Unpackage remifentanil compartments
        x1_remi, x2_remi, x3_remi, Ce_remi = state[4:8]

        # Unpackage Propofol parameters
        v1_prop, k10_prop, k12_prop, k13_prop, k21_prop, k31_prop, ke0_prop = params[0:7]

        # Unpackage Remifentanil parameters
        v1_remi, k10_remi, k12_remi, k13_remi, k21_remi, k31_remi, ke0_remi = params[7:14]

        # Convert amount to concentration for compartment 1
        C1_prop = x1_prop / (v1_prop * 1000.0)
        C1_remi = x1_remi / (v1_remi * 1000.0)

        # Propofol derivatives
        dx1_prop_dt = (
            + u_prop 
            + k21_prop * x2_prop 
            + k31_prop * x3_prop 
            - (k10_prop + k12_prop + k13_prop) * x1_prop
        )
        dx2_prop_dt = k12_prop * x1_prop - k21_prop * x2_prop
        dx3_prop_dt = k13_prop * x1_prop - k31_prop * x3_prop
        dCe_prop_dt = ke0_prop * (C1_prop - Ce_prop)

        # Remifentanil derivatives
        dx1_remi_dt = (
            + u_remi
            + k21_remi * x2_remi
            + k31_remi * x3_remi
            - (k10_remi + k12_remi + k13_remi) * x1_remi
        )
        dx2_remi_dt = k12_remi * x1_remi - k21_remi * x2_remi
        dx3_remi_dt = k13_remi * x1_remi - k31_remi * x3_remi
        dCe_remi_dt = ke0_remi * (C1_remi - Ce_remi)
        
        # Package the derivatives
        return (
            dx1_prop_dt,
            dx2_prop_dt,
            dx3_prop_dt,
            dCe_prop_dt,
            dx1_remi_dt,
            dx2_remi_dt,
            dx3_remi_dt,
            dCe_remi_dt
        )
