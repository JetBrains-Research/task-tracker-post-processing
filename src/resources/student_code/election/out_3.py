def helper_g0(p0_helper_g0, p1_helper_g0, p2_helper_g0):
    if ((p0_helper_g0 == 0) and (p1_helper_g0 == 0)):
        return 0
    elif ((p1_helper_g0 == 0) and (p2_helper_g0 == 0)):
        return 0
    elif ((p0_helper_g0 == 0) and (p2_helper_g0 == 0)):
        return 0
    elif (((p0_helper_g0 == 1) and (p1_helper_g0 == 1)) or ((p0_helper_g0 == 1) and (p2_helper_g0 == 1)) or ((p1_helper_g0 == 1) and (p2_helper_g0 == 1))):
        return 1