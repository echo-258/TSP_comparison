from sim_ann import SA
from ant_col import AC
import TSP
import matplotlib.pyplot as plt
from multiprocessing import Process


def plot_iter_cost(algo_inst):
    ''' 画出迭代的收敛曲线 '''

    x = list(range(len(algo_inst.costs)))
    y = algo_inst.costs
    img_name = str(algo_inst.__class__.__name__).lower()

    cost_img = plt.figure(figsize=(40, 20))
    plt.plot(x, y, color='b')
    plt.rcParams.update({"font.size": 20})  # 此处必须添加此句代码方可改变标题字体大小
    plt.title('Map NO.' + str(algo_inst.TSP.cnt) + ' ' + algo_inst.__class__.__name__, fontsize=40)
    plt.xlabel('iters', fontsize=30)
    plt.ylabel('cost', fontsize=30)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    cost_img.savefig(fname='Map No_' + str(algo_inst.TSP.cnt) + ' ' + img_name+'_cost')

def sa_test(tsp_inst):
    sa = SA(100000, 20, 0.99, tsp_inst, 5000)
    # sa = SA(1000, 1, 0.9, tsp_inst, 1000)
    sa_time = sa.solve()
    plot_iter_cost(algo_inst=sa)
    sa.TSP.plot_path(algo='sa')
    # Process(target=sa.plot_iter_cost()).start() #实例化进程对象
    # Process(target=TSP.plot_path(2)).start()   #实例化进程对象
    return sa.TSP.path, sa.TSP.path_cost, sa_time

def ac_test(tsp_inst):
    ac = AC(50, 2, 4, 0.5, 1, tsp_inst, 50)
    # ac = AC(10, 1, 1, 0.1, 2, tsp_inst, 100)
    ac_time = ac.solve()
    plot_iter_cost(algo_inst=ac)
    ac.TSP.plot_path(algo='ac')
    # Process(target=ac.plot_iter_cost).start()
    # Process(target=TSP.plot_path(4)).start()
    return ac.TSP.path, ac.TSP.path_cost, ac_time

if __name__ == "__main__":
    sa_cost_list, ac_cost_list = [], []
    map_num = 10
    city_num = 100
    for i in range(map_num):
        TSP_Inst = TSP.TSP_inst(cnt=i + 1, num=city_num)
        # print(TSP_Inst.cities)
        sa_path, sa_cost, sa_time = sa_test(TSP_Inst)
        ac_path, ac_cost, ac_time = ac_test(TSP_Inst)
        sa_cost_list.append(sa_cost)
        ac_cost_list.append(ac_cost)
        with open('result.txt', 'a+') as fout:
            fout.write("====================Map NO.{}====================\n".format(i + 1))
            fout.write(str(TSP_Inst.cities))
            fout.write("\nsa:\tpath:{}\n\tcost:{}\n\ttime:{:.4}s\n".format(sa_path, sa_cost, sa_time))
            fout.write("ac:\tpath:{}\n\tcost:{}\n\ttime:{:.4}s\n\n\n".format(ac_path, ac_cost, ac_time))

    cmp_img = plt.figure(figsize=(40, 20))
    name = [str(k) for k in range(1, map_num + 1)]
    total_width, n = 0.8, 2
    width = total_width / n
    x = list(range(map_num))

    a = plt.bar(x, sa_cost_list, width=width, label='sa_cost', fc='red')
    for i in range(map_num):
        x[i] = x[i] + width
    b = plt.bar(x, ac_cost_list, width=width, label='ac_cost', tick_label=name, fc='blue')

    for rect in a:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%.3f' % float(height))
    for rect in b:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%.3f' % float(height))

    plt.xlabel('Maps')
    plt.ylabel('Cost')
    plt.title('Cost Comparison between SA & AC')
    plt.legend()
    cmp_img.savefig('cost_cmp')
