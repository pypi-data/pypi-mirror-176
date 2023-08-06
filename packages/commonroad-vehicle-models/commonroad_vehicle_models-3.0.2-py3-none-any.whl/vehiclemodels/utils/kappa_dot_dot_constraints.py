import math


def kappa_dot_dot_constraints(kappa_dot_dot, kappa_dot, p):

    if (kappa_dot < -p.steering.kappa_dot_max and kappa_dot_dot < 0.) \
            or (kappa_dot > p.steering.kappa_dot_max and kappa_dot_dot > 0.):
        kappa_dot_dot = 0.

    l_wb = p.a + p.b
    kappa_min = math.tan(p.steering.min) / l_wb
    kappa_max = math.tan(p.steering.max) / l_wb
    # TODO consider constraints on kappa
    return kappa_dot_dot
