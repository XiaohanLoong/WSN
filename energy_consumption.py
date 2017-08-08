# 所有节点同时消耗能量，在网络初始化阶段可能会有
# energy：能量列表
# comsumption：消耗的能量
def comsume_energy_all(energy, comsumption, total_energy_comsuption):
    for i in range(len(energy)):
        total_energy_comsuption[0] += comsumption
        energy[i] -= comsumption


# 单个节点同时消耗能量
# energy：能量列表
# id：节点id，就是列表的下标
# comsumption：消耗的能量
def comsume_energy_someone(energy, id, comsumption, total_energy_comsuption):
    total_energy_comsuption[0] += comsumption
    energy[id] -= comsumption
