import auv_position
import tools


# 节点计算自己的类型
# nodes：节点列表
# node_type: 节点类型列表
# phi：AUV当前周期的初始相位
# rho:AUV圆周运动的径长
# omega:AUV圆周运动的角速度
# v_h：AUV垂直方向的速度
# r：节点的通信半径
# d：安全距离
# h；网络深度
# flag：标志为，如果为正，表示AUV在下潜，否则为上浮。
def judge_node_type(nodes, node_type, phi, rho, omega, v_h, r, d, h, flag):
    number = len(nodes[0])
    for i in range(number):
        # 如果节点与sink节点的距离小于等于通信半径，则为直接送达节点。这边本来应该是 <=r ,为了简单直接用安全距离。
        if tools.get_distance(nodes[0][i], nodes[1][i], nodes[2][i], 0, 0,
                              0) <= d:
            node_type[i] = 2
            continue
        # 解微分方程的方式求解太过麻烦，直接暴力破解。
        t_max = h / v_h
        min_distance = 65536
        for t in range(int(t_max)):
            auv_x, auv_y, auv_z = auv_position.get_auv_position_at_time_t(t,
                                                                          phi,
                                                                          rho,
                                                                          omega,
                                                                          v_h,
                                                                          h,
                                                                          flag)
            distance = tools.get_distance(nodes[0][i], nodes[1][i], nodes[2][i],
                                          auv_x, auv_y, auv_z)
            min_distance = distance if min_distance >= distance else min_distance
        if min_distance <= d:
            node_type[i] = 1
