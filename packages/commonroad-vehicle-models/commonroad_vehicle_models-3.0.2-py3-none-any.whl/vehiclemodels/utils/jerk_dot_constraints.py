

def jerk_dot_constraints(jerk_dot, jerk, acceleration, p):

    # TODO!!!!!!!!!!!!!!

    if (jerk_dot < 0. and acceleration <= -p.a_max) or (jerk_dot > 0. and acceleration >= p.a_max):
        # acceleration limit reached
        jerk_dot = 0.
    elif (jerk_dot < 0. and jerk <= -p.j_max) or (jerk_dot > 0. and jerk >= p.j_max):
        # jerk limit reached
        jerk_dot = 0.
    # elif abs(jerk_dot) >= p.jerk_dot_max:
    #     # jerk_dot limit reached
    #     jerk_dot = 0.
    return jerk_dot
