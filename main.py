import node_init
import energy_consumption
import math
import random
import send_data
import is_end
import sys
import judge_type

sys.setrecursionlimit(10000000)
# 网络区域长度
l = 1500
# 网络区域宽度
w = 1500
# 网络区域深度
h = 1500
# 网络中节点个数
node_number = 500
# AUV圆周运动的径长
rho = l / 4.0
# AUV圆周运动的初始相位
phi = 0.0
# AUV的上浮或者下潜的速度
v_h = 1.0
# AUV从顶部运行到底部的圆周运动的周期数
n = 2
# 安全时间，计算方法为数据包长度/数据包发送速度，这边假设为5s.
t_safe = 5.0
# AUV圆周运动的角速度，选择这个速度是为了使得AUV到达底部的相位与初始相位一致。
omega = v_h * 2 * math.pi * n / h
# 节点的通信半径
r = 200.0
# 安全距离
d = math.sqrt(r ** 2 - ((omega * rho * t_safe) / 2) ** 2)

# 最大跳数
k = (l ** 2 + w ** 2 + h ** 2) ** 0.5 / 200.0

# 每秒有多少个节点有数据包要发送。
percentage_of_source_node_per_second = 0.8
# 网络死亡时sink节点和auv接收到的总的数据包个数
total_data_packs_number = [0]
# 网络死亡时网络消耗的总能量
total_energy_comsumption = [0]

# 节点每发送1bit的数据需要消耗6,3mJ的能量
energy_consumption_per_bit_send = 6.3 * (10 ** -6)
# 节点每接收1bit的数据需要消耗0mJ的能量
energy_consumption_per_bit_rece = 0
# 数据包的长度
data_packs_length = 2500
# 控制包的长度
control_packs_length = 64

# 节点被随机部署在网络中
nodes = node_init.init(l, w, h, node_number)
# 节点类型，0表示普通节点，1表示网关节点，2表示直接送达节点
node_type = [0 for i in range(node_number)]

# 节点初始能量100.0J
energy = [100.0 for i in range(node_number)]
# AUV的初始位置
auv_position_coordinates = [[rho], [0], [0]]

# 网络初始化阶段，sink节点将AUV的移动参数进行全网广播
energy_consumption.comsume_energy_all(energy,
                                      energy_consumption_per_bit_rece * control_packs_length,
                                      total_energy_comsumption)


# 网络的生存时间


def main():
    total_time = 0
    # 网络开始运行，到第一个节点死亡结束
    t = 0
    while True:
        # auv_position_coordinates[0], auv_position_coordinates[1], \
        # auv_position_coordinates[
        #     2] = auv_position.get_auv_position_at_time_t(t, phi, rho, omega, v_h, h)
        flag = True
        if t >= h / v_h:
            flag = not flag
            t = 0
        judge_type.judge_node_type(nodes, node_type, phi, rho, omega, v_h, r, d,
                                   h,
                                   flag)
        for i in range(node_number):
            if random.uniform(0, 1) <= percentage_of_source_node_per_second:
                send_data.send_data(nodes, i, node_type, d, energy,
                                    energy_consumption_per_bit_send * data_packs_length,
                                    energy_consumption_per_bit_rece * data_packs_length,
                                    phi, rho, omega, v_h, h, flag,
                                    total_data_packs_number,
                                    total_energy_comsumption, 4)
                # 节点发送数据
                # send_data.send_data(nodes, i, node_type, d, energy,
                #                     energy_consumption_per_bit_send * data_packs_length,
                #                     energy_consumption_per_bit_rece * data_packs_length,
                #                     phi, rho, omega, v_h, h, True,
                #                     total_data_packs_number)
                pass
        t += 1
        total_time += 1
        if is_end.is_network_end(energy):
            break
    print(total_time)
    print(total_data_packs_number)
    print(total_energy_comsumption)


def test():
    send_data.send_data(nodes, 1, energy,
                        energy_consumption_per_bit_send * data_packs_length,
                        energy_consumption_per_bit_rece * data_packs_length,
                        total_energy_comsumption,
                        total_data_packs_number, 4)


if __name__ == '__main__':
    main()
