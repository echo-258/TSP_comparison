import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

#蚁群算法ACO(Ant Colony Optimization)
class AC():

    def __init__(self,
                 ants_num,  # 蚂蚁数量
                 alpha,  # 信息素影响因子
                 beta,  # 可见度影响因子
                 Rho,  # 信息素挥发率
                 Q,  # 信息素释放的量  常量
                 TSP,  # TSP实例
                 iteration=1000  # 迭代次数
                 ):

        self.ants_num = ants_num
        self.alpha = alpha
        self.beta = beta
        self.Rho = Rho
        self.Q = Q
        self.TSP = TSP
        self.iteration = iteration  # 迭代次数
        self.costs = []

    def cal_newpath(self, dis_mat, path_new):
        dis_list = []
        for each_ant in path_new:
            dis = 0
            for j in range(self.TSP.city_nums - 1):
                dis = dis_mat[each_ant[j]][each_ant[j + 1]] + dis
            dis = dis_mat[each_ant[self.TSP.city_nums - 1]][each_ant[0]] + dis  # 回家
            dis_list.append(dis)
        return dis_list

    def solve(self):
        ''' 执行蚁群算法'''
        # --------------------------初始化
        dist_mat = np.array(self.TSP.distance)  # 距离矩阵

        e_mat_init = 1.0 / (dist_mat + np.diag([10000] * self.TSP.city_nums))
        diag = np.diag([1.0 / 10000] * self.TSP.city_nums)
        e_mat = e_mat_init - diag  # 可见度矩阵 中间为避免“除以零”错误，在对角线（表示城市到自己的距离）暂时填充了数字

        pheromone_mat = np.ones((self.TSP.city_nums, self.TSP.city_nums))  # 信息素浓度矩阵
        path_mat = np.zeros((self.ants_num, self.TSP.city_nums)).astype(int)  # 路径矩阵

        start_t = time.time()

        print("======================[ AC ]===========================")

        for count in range(self.iteration):  # ----------------第一层循环
            for ant in range(self.ants_num):    # ----------------第二层循环
                visit = random.randint(0, self.TSP.city_nums - 1)   # 每次每只蚂蚁从随机城市出发
                path_mat[ant][0] = visit
                unvisit_list = list(range(0, self.TSP.city_nums))  # 未访问的城市
                unvisit_list.remove(visit)                         # 除去起始城市
                for city_num in range(1, self.TSP.city_nums):  # --------------第三层循环
                    # 轮盘法选择下一个城市
                    prbb_list = []
                    prbb_sum = 0
                    for k in range(len(unvisit_list)):
                        prbb_sum += np.power(pheromone_mat[visit][unvisit_list[k]], self.alpha) * np.power(
                            e_mat[visit][unvisit_list[k]], self.beta)
                        prbb_list.append(prbb_sum)

                    rand = random.uniform(0, prbb_sum)  # 产生随机数

                    for t in range(len(prbb_list)):
                        if rand <= prbb_list[t]:
                            visit_next = unvisit_list[t]
                            break
                        else:
                            continue
                    path_mat[ant][city_num] = visit_next  # 填路径矩阵

                    unvisit_list.remove(visit_next)  # 更新：除去新访问到的城市
                    visit = visit_next  # 更新：从新房闻到的城市开始探索下一个城市

            # 所有蚂蚁的路径表填满之后，算每只蚂蚁走过的总距离
            dis_all = self.cal_newpath(dist_mat, path_mat)

            # 每次迭代更新最短距离和最短路径
            if count == 0:
                dis_new = min(dis_all)
                path_new = path_mat[dis_all.index(dis_new)].copy()
            else:
                if min(dis_all) < dis_new:
                    dis_new = min(dis_all)
                    path_new = path_mat[dis_all.index(dis_new)].copy()

            # 更新信息素矩阵
            pheromone_change = np.zeros((self.TSP.city_nums, self.TSP.city_nums))
            for i in range(self.ants_num):
                for j in range(self.TSP.city_nums - 1):
                    pheromone_change[path_mat[i, j]][path_mat[i, j + 1]] += self.Q / dis_all[i]
                pheromone_change[path_mat[i, self.TSP.city_nums - 1]][path_mat[i, 0]] += self.Q / dis_all[i]
            pheromone_mat = (1 - self.Rho) * pheromone_mat + pheromone_change

            self.costs.append(dis_new)
            print("[{}] path:{}      cost:{}".format(count, path_new, dis_new).replace("\n", ''))

        end_t = time.time()
        # 最后结果
        self.TSP.path = path_new.tolist()       # 转为列表格式
        self.TSP.path_cost = dis_new

        print("=============[ path:{} cost:{}  time:{:.4}s]===============".format(self.TSP.path, self.TSP.path_cost,
                                                                                   end_t - start_t))

        return end_t - start_t
