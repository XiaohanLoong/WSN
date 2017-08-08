import random


# 节点随机部署
# l:网络区域的长度
# w:网络区域的宽度
# h:网络区域的深度
# number:节点的个数
# return:一个三行number的列表。第一行为节点的x坐标，第二行为节点的y坐标，第三行为节点的z坐标。
def init(l, w, h, number):
    nodes = [[0 for col in range(number)] for row in range(3)]
    for i in range(number):
        # 柱坐标生成不太方便，直接使用直角坐标。需要计算时将AUV的坐标转换为直角坐标。
        # x = (l / 2.0) * random.uniform(-1, 1)
        # y = (w / 2.0) * random.uniform(-1, 1)
        # nodes[0][i] = math.sqrt(x ** 2 + y ** 2)
        # nodes[1][i] = math.degrees(math.acos(x / math.sqrt(x ** 2 + y ** 2)))
        # nodes[2][i] = h * random.uniform(0, 1)
        nodes[0][i] = (l / 2.0) * random.uniform(-1, 1)
        nodes[1][i] = (w / 2.0) * random.uniform(-1, 1)
        nodes[2][i] = h * random.uniform(0, 1)
    return nodes
