from myelin import PatientLoader
import json

def _lbm(weight, height, sex):
    """Lean body mass (James formula). sex: 1=male, 0=female."""
    if sex == 1:
        return 1.1 * weight - 128 * (weight / height) ** 2
    else:
        return 1.07 * weight - 148 * (weight / height) ** 2

def schnider_params(age, weight, height, sex):
    """
    Schnider propofol PK parameters.
    Returns (v1, k10, k12, k13, k21, k31, ke0) in units of L and 1/min.
    """
    lbm = _lbm(weight, height, sex)

    cl1 = 1.89 + 0.0456 * (weight - 77) - 0.0681 * (lbm - 59) + 0.0264 * (height - 177)
    cl2 = 1.29 - 0.024 * (age - 53)
    cl3 = 0.836

    v1 = 4.27
    v2 = 18.9 - 0.391 * (age - 53)
    v3 = 238.0

    ke0 = 0.456  # 1/min

    k10 = cl1 / v1
    k12 = cl2 / v1
    k13 = cl3 / v1
    k21 = cl2 / v2
    k31 = cl3 / v3

    return (v1, k10, k12, k13, k21, k31, ke0)

def minto_params(age, weight, height, sex):
    """
    Minto remifentanil PK parameters.
    Returns (v1, k10, k12, k13, k21, k31, ke0) in units of L and 1/min.
    """
    lbm = _lbm(weight, height, sex)

    cl1 = 2.6 - 0.0162 * (age - 40) + 0.0191 * (lbm - 55)
    cl2 = 2.05 - 0.0301 * (age - 40)
    cl3 = 0.076 - 0.00113 * (age - 40)

    v1 = 5.1 - 0.0201 * (age - 40) + 0.072 * (lbm - 55)
    v2 = 9.82 - 0.0811 * (age - 40) + 0.108 * (lbm - 55)
    v3 = 5.42

    ke0 = 0.595 - 0.007 * (age - 40)  # 1/min

    k10 = cl1 / v1
    k12 = cl2 / v1
    k13 = cl3 / v1
    k21 = cl2 / v2
    k31 = cl3 / v3

    return (v1, k10, k12, k13, k21, k31, ke0)

def bouillon_params(age, weight, height, sex):
    """
    Bouillon BIS surface-response PD parameters.
    Returns (e0, emax, c50_prop, c50_remi, gamma).

    These are population means from Bouillon et al. (2004).
    """
    e0 = 93.0  # awake BIS
    emax = 93.0  # maximum drug effect (BIS -> 0)
    c50_prop = 3.08  # µg/mL propofol Ce at half-effect
    c50_remi = 12.7  # ng/mL remifentanil Ce at half-effect (normalized)
    gamma = 1.43  # Hill coefficient

    return (e0, emax, c50_prop, c50_remi, gamma)

class PASPatientLoader(PatientLoader):
    default_id = ('adults', 1)

    def load(self, patient_id):
        """
        Compute all 19 plant params from patient demographics.

        params[0:7] — Schnider propofol PK (v1, k10, k12, k13, k21, k31, ke0)
        params[7:14] — Minto remifentanil PK (v1, k10, k12, k13, k21, k31, ke0)
        params[14:19] — Bouillon BIS PD (e0, emax, c50_prop, c50_remi, gamma)
        """
        cohort, pid = patient_id
        with open(f'cohorts/{cohort}/{pid}.json') as f:
            p = json.load(f)

        age, weight, height, sex = p['age'], p['weight'], p['height'], p['sex']

        prop_pk = schnider_params(age, weight, height, sex)
        remi_pk = minto_params(age, weight, height, sex)
        bis_pd = bouillon_params(age, weight, height, sex)

        return prop_pk + remi_pk + bis_pd
