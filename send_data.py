import auv_position
import energy_consumption
import tools


def send_data(nodes, node_id, node_type, d, energy, energy_consumption_send,
              energy_consumption_rece,
              phi, rho, omega, v_h, h, flag, total_data_packs_number,
              total_energy_comsuption, k):
    if k <= 0:
        return
        # 接收到数据包，消耗能量
    energy_consumption.comsume_energy_someone(energy, node_id,
                                              energy_consumption_rece,
                                              total_energy_comsuption)
    # 网关节点或者直接送达节点
    if node_type[node_id] != 0:
        energy_consumption.comsume_energy_someone(energy, node_id,
                                                  energy_consumption_send,
                                                  total_energy_comsuption)
        total_data_packs_number[0] += 1
        return

    # 获得AUV到达本深度时的位置
    t = nodes[2][node_id] / v_h if flag else (h - nodes[2][node_id]) / v_h
    auv_x, auv_y, auv_z = auv_position.get_auv_position_at_time_t(t, phi, rho,
                                                                  omega, v_h, h,
                                                                  flag)
    send_data(nodes,
              get_neighbors(nodes, node_id, node_type, d, auv_x, auv_y, auv_z,
                            energy), node_type, d, energy,
              energy_consumption_send,
              energy_consumption_rece,
              phi, rho, omega, v_h, h, flag, total_data_packs_number,
              total_energy_comsuption, k - 1)
    # next_id = 0
    # distance = 65536
    # for i in range(len(nodes[0])):
    #     if tools.get_distance(nodes[0][node_id], nodes[1][node_id],
    #                           nodes[2][node_id],
    #                           nodes[0][i], nodes[1][i], nodes[1][i]) <= d:
    #         if node_type[i] != 0:
    #             energy_consumption.comsume_energy_someone(energy, node_id,
    #                                                       energy_consumption_send)
    #             total_data_packs_number[0] += 1
    #             print("receive")
    #             return
    #         dis = tools.get_distance(nodes[0][i], nodes[1][i], nodes[2][i],
    #                                  auv_x,
    #                                  auv_y, auv_z)
    #         if dis <= distance:
    #             distance = dis
    #             next_id = i
    #         energy_consumption.comsume_energy_someone(energy, node_id,
    #                                                   energy_consumption_send)
    #         send_data(nodes, next_id, node_type, d, energy,
    #                   energy_consumption_send,
    #                   energy_consumption_rece,
    #                   phi, rho, omega, v_h, h, flag, total_data_packs_number)


# pass

# def send_data(nodes, node_id, energy, energy_comsumption_send,
#               energy_comsumption_rece,
#               total_energy_comsumption, total_data_packs_number, k):
#     if k <= 0:
#         # print("数据过期了")
#         return
#     if tools.get_distance(nodes[0][node_id], nodes[1][node_id],
#                           nodes[2][node_id], 0, 0, 0) <= 200:
#         # print('直接发送')
#         energy_consumption.comsume_energy_someone(energy, node_id,
#                                                   energy_comsumption_send)
#         print('sink节点收到数据')
#         total_energy_comsumption[0] += energy_comsumption_send
#         total_data_packs_number[0] += 1
#     else:
#         # print('间接发送')
#         neighbors_id = get_neighbors(nodes, node_id)
#         if neighbors_id != -1:
#             # print('向邻居节点转发数据，当前节点深度')
#             send_data(nodes, neighbors_id, energy, energy_comsumption_send,
#                       energy_comsumption_rece,
#                       total_energy_comsumption, total_data_packs_number, k - 1)
#             energy_consumption.comsume_energy_someone(energy, node_id,
#                                                       energy_comsumption_send)
#             total_energy_comsumption[0] += energy_comsumption_send
#         else:
#             # print('局部最优解')
#             pass
#
#
def get_neighbors(nodes, node_id, node_type, d, auv_x, auv_y, auv_z, energy):
    max_weight = 0
    neighbor_id = -1
    for i in range(len(nodes[0])):
        if tools.get_distance(nodes[0][node_id], nodes[1][node_id],
                              nodes[2][node_id], nodes[0][i], nodes[1][i],
                              nodes[2][i]) <= d:
            if node_type[i] != 0:
                return i
            weight = energy[i] / tools.get_distance(nodes[0][i], nodes[1][i],
                                                    nodes[2][i], auv_x, auv_y,
                                                    auv_z)
            max_weight, neighbor_id = (weight, i) if weight > max_weight else (
                max_weight, neighbor_id)
    return neighbor_id
