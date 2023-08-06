import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import copy
from geopy.distance import geodesic
import heapq
from sklearn.neighbors import NearestNeighbors
from scipy.optimize import curve_fit
from scipy.spatial.distance import cdist

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class U_ST:      #univariate Space&Time
    #distances, indices, distances_k, indices_k=[],[],[],[]
    #l0,l=0,0
    #weight_list, weight_index, P=[],[],[]
    #C0=0
    #cc,C,A,B,x,y#=0,0,0,0,[],[]

    def __init__(self):
        self.distances, self.indices, self.distances_k, self.indices_k = [], [], [], []
        self.l0, self.l = 0, 0
        self.weight_list, self.weight_index, self.P = [], [], []
        self.C0 = 0
        self.cc, self.C, self.A, self.B, self.x, self.y = 0, 0, 0, 0, [], []

    # -----------------------------------------------------------------------------------------------------------定义抽象的函数
    # --------------------------------------------------------------------------------------------------计算k近邻
    def nbrs_k(self, n_k, count_k, k):
        nbrs = NearestNeighbors(n_neighbors=n_k, algorithm='ball_tree').fit(count_k)
        distances, indices = nbrs.kneighbors(count_k)
        distances_k, indices_k = np.array(copy.copy(distances[:, 1:k])), np.array(copy.copy(indices[:, 1:k]))
        return distances, indices, distances_k, indices_k

    # --------------------------------------------------------------------------------------------------计算l与l0
    def l0_l(self, distances_k):
        l0 = np.mean(distances_k)
        l = pow(2, 0.5) * l0  # l表示基本游动区间半径
        return l0, l

    # --------------------------------------------------------------------------------------------------计算权重
    def weight(self, count, distances, indices, l0, l):
        weight_list, weight_index, P = [], [], []  # 待计算权重的距离值及待计算权重的点号
        for m in range(count):
            list = distances[m]  # 矩阵形式
            list = list.tolist()
            weight_list.append([t for t in list if t < l])  # 寻找游动区间内的点的距离
            weight_index.append(indices[m][0:len(weight_list[m])])
            P_pa = []
            for i in range(len(weight_index[m])):  # 计算权重
                P_pa.append(4 * math.exp(-0.693 * (weight_list[m][i] / l0) * (weight_list[m][i] / l0)))
            P.append(P_pa)
        return weight_list, weight_index, P

    # --------------------------------------------------------------------------------------------------滤波
    def lvbo(self, data, count1, count2, weight_index, P, C0):  # 定义滤波函数
        G, R, G_list = 0, 0, []
        for t in range(count1):
            G_list_ave = []
            for m in range(count2):
                pq = 0
                for n in range(len(weight_index[m])):  # len(index_weight[m])为游动区间内点的个数
                    pq = pq + P[m][n] * data[t][weight_index[m][n]]  # 算出pq的和
                G_list_ave.append(pq / sum(P[m]))  # 算出新的q值
            G_list.append(G_list_ave)
        G = np.mean(np.var(G_list, axis=1))  # 算出G(L)
        R = C0 - G
        return G_list, R

    def filter(self, data, count1, count2, weight_index, P, C0):
        R1, R2 = 0, 1
        G1list = []  # k-1遍滤波的q值
        G2list = copy.copy(data)  # k遍滤波的q值
        RL_list = [0]  # 记录所有的R(L)值
        lvbo_count, filter_count = 0, 0
        while (R2 - R1) / R2 > 0.03:  # 滤波终止条件：Ta=(R2-R1)/R2<=0.08,多滤几遍
            R1 = R2
            G1list = copy.copy(G2list)
            G2list, R2 = self.lvbo(G1list, count1, count2, weight_index, P, C0)
            RL_list.append(R2)
            lvbo_count = lvbo_count + 1
            if ((R2 - R1) / R2 > 0.08):  # 滤波终止条件：Ta=(R2-R1)/R2<=0.08
                filter_count = filter_count + 1
        return filter_count + 1, lvbo_count, RL_list,

    # -------------------------------------------------------------------------------------------------求解c
    def Cal_C(self, C0, cc, lvbo_count, L):
        VR = cc / (C0 * lvbo_count * L)
        c = 2 * (1 - VR)  # 0.5<=c<=1.5
        c = round(c, 3)
        if c > 1.5 or c < 0.5:
            c = 1
        return c

    # -------------------------------------------------------------------------------------------------求解参数
    def func_(self, x, A, B):
        x = x + 0.001
        return A * np.exp(-B / x ** self.C)


    # -------------------------------------------------------------------------------------------------拟合曲线
    def curve(self, RL_list, l, func):
        x, y = [], []
        for i in range(len(RL_list)):
            x.append(i * l)
        popt, pcov = curve_fit(func, x, RL_list, [1000, 1])
        A, B = popt[0], popt[1]
        for i in range(len(x)):
            y.append(func(x[i], A, B))
        return A, B, x, y

    # -------------------------------------------------------------------------------------------------绘制曲线
    x_tick = [0, 'l', '2l', '3l', '4l', '5l', '6l', '7l', '8l', '9l', '10l', '11l', '12l', '13l', '14l', '15l', '16l',
              '17l', '18l', '19l', '20l']

    def plot_curve(self, C0, x, y, RL_list, func, A, B, l, filter_count):
        print("\tl(X值): ", x)
        print("\tR(l)(计算值）: ", RL_list)
        print("\tR(l)(拟合值）：", y)

        fig = plt.figure(figsize=(8, 6), dpi=100)
        plt.axhline(y=C0, color='black', linestyle='-', alpha=0.2)
        plt.axhline(y=C0 / 2, color='black', linestyle='-', alpha=0.2)
        plt.axvline(x=l * filter_count, color='red', linestyle='-', alpha=0.2)

        plot1 = plt.plot(x, RL_list, 'o', label='计算值')
        plot2 = plt.plot(x, y, 'r-', label='拟合值')

        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xticks(x, self.x_tick[:len(x)])
        plt.legend(loc='best')

