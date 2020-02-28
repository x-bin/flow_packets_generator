import json
import numpy as np

class concurrency_flows_num:
    def __init__(self, filename, filetype):
        self.filename = filename
        self.pkts = None
        self.len_pkts = 0
        self.flow_begin_end = dict()
        self.flow_nums = 0
        self.concurrency_flows_num = None
        if filetype == 0:
            self.read_from_file()
        else:
            self.read_from_hgc()
        self.calculate_flow_begin_end()
        #self.show_cumulative_distribution_function()

    def read_from_file(self):
        with open(self.filename, "r") as f:
            self.pkts = json.load(f)
            self.len_pkts = len(self.pkts)
            print("数据包总量为：", self.len_pkts)

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
                temp = srcip + '\t' + dstip + '\t' + proto + '\t' + srcport + '\t' + dstport
                self.pkts.append(temp)
            self.len_pkts = len(self.pkts)
            print("数据包总量为：", self.len_pkts)
        file = "/Users/xiongbin/CAIDA/HGC.20080415001.dict.json"
        with open(file, "r") as f:
            pkts = json.load(f)
            for i in range(len(pkts)):
                srcip = pkts[i]["srcip"]
                dstip = pkts[i]["dstip"]
                proto = pkts[i]["proto"]
                srcport = pkts[i]["srcport"]
                dstport = pkts[i]["dstport"]
                temp = srcip + '\t' + dstip + '\t' + proto + '\t' + srcport + '\t' + dstport
                self.pkts.append(temp)
            self.len_pkts = len(self.pkts)
            print("数据包总量为：", self.len_pkts)

    def calculate_flow_begin_end(self):
        for i in range(self.len_pkts):
            if self.pkts[i] in self.flow_begin_end:
                self.flow_begin_end[self.pkts[i]][1] = i
            else:
                self.flow_begin_end[self.pkts[i]] = [i, i]

        vals = list(self.flow_begin_end.values())
        self.flow_nums = len(vals)
        print("流个数为：", self.flow_nums)
        self.concurrency_flows_num = np.zeros(self.len_pkts)
        '''
        for i in range(self.flow_nums):
            print(i)
            st = np.zeros(vals[i][0])
            bw = np.ones(vals[i][1] + 1 - vals[i][0])
            ed = np.zeros(self.len_pkts - vals[i][1] - 1)
            temp = np.concatenate((st,bw,ed))
            self.concurrency_flows_num = self.concurrency_flows_num + temp
        '''
        begin = 10000000
        num = 10000
        end = begin + num
        c1 = np.zeros(num)
        for i in range(begin, end):
            for j in range(self.flow_nums):
                if vals[j][0] <= i <= vals[j][1]:
                    c1[i-begin] += 1
            print(i, c1[i-begin])
        print("均值为：", np.mean(c1))

    def show_cumulative_distribution_function(self):
        X = list(self.flow_distribution.keys())
        Y = list(self.flow_distribution.values())
        X = np.asarray(X)
        Y = np.asarray(Y)
        for i in range(0, len(X)):
            for j in range(i + 1, len(X)):
                Y[i] += Y[j]
        Y = np.log(Y / self.flow_nums)
        X = np.log(X)
        plt.plot(X, Y)

        k, b = optimize.curve_fit(f1, X, Y)[0]
        print(k, b, np.exp(-k / b))
        x1 = np.linspace(0, 15, 100)
        y1 = k * x1 + b
        plt.plot(x1, y1, color="r")

        k2 = optimize.curve_fit(f2, X, Y)[0]
        print(k2)
        y2 = k2 * x1
        plt.plot(x1, y2, color="g")

        plt.show()


if __name__ == "__main__":
    #filename = "/Users/xiongbin/CAIDA/CAIDA.equinix-nyc.dirA.20180315-125910.UTC.anon.clean.json"
    filename = "/Users/xiongbin/CAIDA/HGC.20080415000.dict.json"
    re = concurrency_flows_num(filename, 1)



