def is_network_end(energy):
    min_energy = 100
    for item in energy:
        min_energy = item if item <= min_energy else min_energy
    print('当前最小能量%f' % min_energy)
    # for item in energy:
    #     if item <= 0:
    #         return True
    #return False
    return min_energy <= 0
