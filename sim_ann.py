import random
import math
import time
import matplotlib.pyplot as plt

#模拟退火算法SAA(Simulate Anneal Arithmetic)
class SA():

    def __init__(self,
                 init_t,  # 初始温度
                 lowest_t,  # 最低温度
                 rate,  # 降温系数
                 TSP,  # TSP实例
                 iteration=1000  # 迭代次数
                 ):

        self.current_t = init_t  # 当前温度为初始温度
        self.lowest_t = lowest_t
        self.rate = rate
        self.TSP = TSP
        self.iteration = iteration
        self.costs = []

    def solve(self):
        ''' 执行退火算法'''

        self.TSP.set_random_path()  # -------------------初始化

        start_t = time.time()
        print("======================[ SA ]===========================")

        while (self.current_t > self.lowest_t): # ---------------------外循环 改变温度
            print("[current temperature: {}  lowest:{}]".format(self.current_t, self.lowest_t))
            count_iter = 0  # 迭代计数

            while count_iter < self.iteration:  # ---------------------内循环 迭代次数超过某个次数则退出
                # =============随机交换城市=====================
                # i, j, k = 0, 0, 0
                # while j == i or j == k or i == k:
                #     i = random.randint(1, self.TSP.city_nums - 1)
                #     j = random.randint(1, self.TSP.city_nums - 1)
                #     k = random.randint(1, self.TSP.city_nums - 1)
                # path = self.TSP.path.copy()
                # path[i], path[j], path[k] = path[j], path[k], path[i]
                i, j = 0, 0
                while j == i:
                    i = random.randint(1, self.TSP.city_nums - 1)
                    j = random.randint(1, self.TSP.city_nums - 1)
                path = self.TSP.path.copy()
                path[i], path[j] = path[j], path[i]

                # =============计算新距离======================
                new_cost = self.TSP.cal_path_cost(path)  # 计算新花费
                delta = new_cost - self.TSP.path_cost  # 计算花费差

                if delta <= 0:
                    # 接受新解
                    self.TSP.path, self.TSP.path_cost = path, new_cost
                elif math.exp(-delta / self.current_t) > random.random():
                    # 否则按照Metropolis准则接受新解
                    self.TSP.path, self.TSP.path_cost = path, new_cost

                # print("[{}] {}<=>{} path:{} cost:{}".format(count_iter, i, j, self.TSP.path, self.TSP.path_cost))

                count_iter += 1  # 迭代次数增加
            # =================改变温度================
            self.costs.append(self.TSP.path_cost)
            self.current_t = self.rate * self.current_t

        end_t = time.time()

        print("=============[ path:{} cost:{}  time:{:.4}s]===============".format(self.TSP.path, self.TSP.path_cost,
                                                                                   end_t - start_t))

        return end_t - start_t

# 产生一条新的遍历路径P(i+1)，计算路径P(i+1)的长度L( P(i+1))
# 若L(P(i+1))< L(P(i))，则接受P(i+1)为新的路径，否则以模拟退火的那个概率接受P(i+1) ，然后降温
# 重复步骤1，2直到满足退出条件