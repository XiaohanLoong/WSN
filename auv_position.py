import math


# 获得t时刻auv的位置


def get_auv_position_at_time_t(t, phi, rho, omega, v_h, h, flag):
    degree = omega * t + phi
    x = rho * math.cos(degree)
    y = rho * math.sin(degree)
    z = v_h * t if flag else h - v_h * t
    return x, y, z
