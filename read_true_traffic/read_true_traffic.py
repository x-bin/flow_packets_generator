import json
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
from scipy import optimize

def f1(x,k,b):
    return k * x + b

def f2(x,k):
    return k * x

class read_true_traffic:
    def __init__(self, filename, filetype):
        self.filename = filename
        self.pkts = None
        self.len_pkts = 0
        self.flow_size = dict()
        self.flow_nums = 0
        self.flow_distribution = dict()

        if filetype == 0:
            self.read_from_file()
        else:
            self.read_from_hgc()
        self.calculate_flow_size()
        self.show_cumulative_distribution_function()


    def read_from_file(self):
        with open(self.filename, "r") as f:
            self.pkts = json.load(f)
            self.len_pkts = len(self.pkts)
            print("数据包总量为：",self.len_pkts)

    def read_from_hgc(self):
        with open(self.filename, "r") as f:
            pkts = json.load(f)
            self.pkts = []
            for i in range(len(pkts)):
                srcip = pkts[i]["srcip"]
                dstip = pkts[i]["dstip"]
                proto = pkts[i]["proto"]
                srcport = pkts[i]["srcport"]
                dstport = pkts[i]["dstport"]
                temp = srcip + '\t'  + dstip + '\t' + proto + '\t' + srcport + '\t' + dstport
                self.pkts.append(temp)
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
        for i in range(0, len(X)):
            for j in range(i+1, len(X)):
                Y[i] += Y[j]
        Y = np.log(Y / self.flow_nums)
        X = np.log(X)
        plt.plot(X, Y)

        k, b = optimize.curve_fit(f1, X, Y)[0]
        print(k, b, np.exp(-k/b))
        x1 = np.linspace(0, 15, 100)
        y1 = k * x1 + b
        plt.plot(x1, y1, color="r")

        k2 = optimize.curve_fit(f2, X, Y)[0]
        print(k2)
        y2 = k2 * x1
        plt.plot(x1, y2, color="g")

        plt.show()






if __name__ == "__main__":
    filename = "/Users/xiongbin/CAIDA/CAIDA.equinix-nyc.dirA.20180315-125910.UTC.anon.clean.json"
    #filename = "/Users/xiongbin/CAIDA/HGC.20080415001.dict.json"
    re = read_true_traffic(filename, 0)




