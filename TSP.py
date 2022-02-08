import random
import numpy as np
import matplotlib.pyplot as plt

class TSP_inst:
    ''' TSP 问题实例 同时充当一些公共的工具类 '''

    #城市坐标
    # cities = np.array([
    #     [32, 15],
    #     [19, 6],
    #     [27, 10],
    #     [3, 30],
    #     [11, 17]])

    # cities = np.array([
    #     [2716, 1919],
    #     [4742, 53],
    #     [1299, 4910],
    #     [3600, 2793],
    #     [1149, 1994],
    #     [62, 1244],
    #     [3517, 738],
    #     [3362, 2634],
    #     [2126, 3589],
    #     [452, 1368],
    #     [218, 3327],
    #     [2552, 2052],
    #     [2034, 466],
    #     [4802, 1364],
    #     [3031, 1693],
    #     [2118, 2937],
    #     [3655, 3562],
    #     [1209, 4257],
    #     [3028, 1459],
    #     [1163, 3618],
    #     [3011, 3627],
    #     [4807, 140],
    #     [1550, 2537],
    #     [785, 1269],
    #     [4081, 1587],
    #     [2886, 3352],
    #     [1513, 153],
    #     [3637, 2222],
    #     [1011, 3559],
    #     [4074, 849],
    # ])

    def __init__(self, cnt, num=40):
        city_list = []
        for i in range(num):
            while True:
                x, y = random.randint(1, 5000), random.randint(1, 5000)
                if [x, y] in city_list:
                    continue
                else:
                    break
            city_list.append([x, y])
        self.cities = np.array(city_list)
        self.city_nums = self.cities.shape[0]  # 城市的数目
        self._get_distance_mat()  # 获得城市之间距离矩阵
        self.cnt = cnt

    def set_random_path(self):
        ''' 随机初始化路径 '''
        self.path = random.sample(range(self.cities.shape[0]), self.cities.shape[0])  # 初始的路径
        self.path_cost = self.cal_path_cost(self.path)  # 计算路径间的花费
        return self.path.copy()

    def set_path(self, path):
        ''' 设置指定路径 '''
        self.path = path
        self.path_cost = self.cal_path_cost(self.path)  # 计算路径间的花费
        return self.path.copy()

    def _get_distance_mat(self):
        ''' 获得距离矩阵 '''
        num = self.cities.shape[0]
        distMat = np.zeros((num, num))
        for i in range(num):
            for j in range(i, num):
                # 使用范式来求解距离
                distMat[i][j] = distMat[j][i] = np.linalg.norm(self.cities[i] - self.cities[j])
        self.distance = distMat

    def cal_path_cost(self, path):
        ''' 计算路径的距离 '''
        dis = 0
        for i in range(len(path) - 1):
            dis += self.distance[path[i]][path[i + 1]]
        dis += self.distance[path[i + 1]][path[0]]  # 回家
        return dis

    def plot_path(self, algo):
        ''' 画出路径 '''
        # 城市的位置
        path_img = plt.figure(figsize=(40, 20))
        plt.rcParams.update({"font.size": 20})  # 此处必须添加此句代码方可改变标题字体大小
        plt.title('Map NO.'+str(self.cnt)+' '+algo+'_path', fontsize=40)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.scatter(self.cities[:, 0], self.cities[:, 1])
        for i in range(len(self.cities)):
            plt.annotate(i, xy=(self.cities[i][0], self.cities[i][1]), xytext=(self.cities[i][0] + 0.2,
                                                                               self.cities[i][1] + 0.2))

        for i in range(len(self.path) - 1):
            plt.plot([self.cities[self.path[i]][0], self.cities[self.path[i+1]][0]], [self.cities[self.path[i]][1],
                                                                                    self.cities[self.path[i+1]][1]])
        plt.plot([self.cities[self.path[0]][0], self.cities[self.path[i+1]][0]], [self.cities[self.path[0]][1],
                                                                                  self.cities[self.path[i+1]][1]])
        path_img.savefig(fname='Map No_'+str(self.cnt)+' '+algo+'_path')

# def test():
#     tsp_test = TSP_inst()
#     print(tsp_test.distance)
#
# if __name__ == "__main__":
#     test()
