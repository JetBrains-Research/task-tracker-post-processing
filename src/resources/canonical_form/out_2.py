def helper_g0(p0_helper_g0):
    if (p0_helper_g0 != 'Monday'):
        if (p0_helper_g0 != 'Tuesday'):
            if (p0_helper_g0 != 'Wednesday'):
                if (p0_helper_g0 == 'Thursday'):
                    return 4
            else:
                return 3
        else:
            return 2
    else:
        return 1
    return 0
