import json
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt

class read_true_traffic:
    def __init__(self, filename):
        self.filename = filename
        self.pkts = None
        self.len_pkts = 0
        self.flow_size = dict()
        self.flow_nums = 0
        self.flow_distribution = dict()





        self.read_from_file()
        self.calculate_flow_size()
        self.show_cumulative_distribution_function()


    def read_from_file(self):
        with open(self.filename, "r") as f:
            self.pkts = json.load(f)
            self.len_pkts = len(self.pkts)
            print("数据包总量为：",self.len_pkts)

    def calculate_flow_size(self):
        for i in range(self.len_pkts):
            if self.pkts[i] in self.flow_size:
                self.flow_size[self.pkts[i]] += 1
            else:
                self.flow_size[self.pkts[i]] = 1

        vals = sorted(list(self.flow_size.values()),reverse = False)
        self.flow_nums = len(vals)
        ave = mean(vals)
        print("并发流个数为：", self.flow_nums)
        print("平均值为：", ave)
        temp = vals[0]
        self.flow_distribution[temp] = 1
        for i in range(1, len(vals)):
            if vals[i] == temp:
                self.flow_distribution[temp] += 1
            else:
                temp = vals[i]
                self.flow_distribution[temp] = 1


    def show_cumulative_distribution_function(self):
        X = list(self.flow_distribution.keys())
        Y = list(self.flow_distribution.values())
        X = np.asarray(X)
        Y = np.asarray(Y)
        Y = Y / self.flow_nums
        for i in range(1, len(X)):
            Y[i] += Y[i-1]
        plt.rcParams['figure.figsize'] = [100,5]
        plt.scatter(X[:1000], Y[:1000], c = "y")

        pareto_x = np.linspace(1,1200,1000)
        pareto_y = 1 - pareto_x ** (-20/19)
        plt.plot(pareto_x, pareto_y, color = "r")
        plt.hlines(1,0,1200)
        plt.savefig("contrast.png")
        plt.show()






if __name__ == "__main__":
    filename = "/Users/xiongbin/CAIDA/CAIDA.equinix-nyc.dirA.20180315-125910.UTC.anon.clean.json"
    re = read_true_traffic(filename)




