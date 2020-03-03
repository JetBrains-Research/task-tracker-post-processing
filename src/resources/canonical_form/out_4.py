import math
def helper_g1(p0_helper_g1):
    return (p0_helper_g1 * 2)
def helper_g0(p0_helper_g0, p1_helper_g0, p2_helper_g0):
    (((- p1_helper_g0) + math.sqrt(((p1_helper_g0 * p1_helper_g0) - (helper_g1(p0_helper_g0) * helper_g1(p2_helper_g0))))) / helper_g1(p0_helper_g0))