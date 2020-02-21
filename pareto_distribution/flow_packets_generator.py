import numpy as np

class flow_packets_generator:
    def __init__(self, flow_nums, min_num, alpha):
        self.flow_nums = flow_nums
        self.min_num = min_num
        self.alpha = alpha
        self.flow_distribution = None
        self.flowid = []
        self.pkts_sequence = []
        self.get_flow_distribution()
        self.get_pkts_sequence()

    def get_flow_distribution(self):
        self.flow_distribution = np.floor((np.random.pareto(self.alpha, size=self.flow_nums) + 1) * self.min_num).astype(int)
        sorted_distribution = np.sort(self.flow_distribution)
        flow_dict = dict()
        temp = sorted_distribution[0]
        flow_dict[temp] = 1
        for i in range(1, len(sorted_distribution)):
            if sorted_distribution[i] == temp:
                flow_dict[temp] += 1
            else:
                temp = sorted_distribution[i]
                flow_dict[temp] = 1
        print("生成的流的具体分布为：")
        for key, value in flow_dict.items():
            print(key, value)
        self.pkts_num = sum(self.flow_distribution)
        print("总数据包的数量为：", self.pkts_num)
        print("每个流的平均数据包量为：", self.pkts_num / self.flow_nums)

    def get_pkts_sequence(self):
        for i in range(self.flow_nums):
            self.flowid.append(self.get_rand_flowid())
            #print(self.flowid[i])
        pkts_num_now = self.pkts_num
        flow_distribution_now = self.flow_distribution
        for i in range(self.pkts_num):
            assert(pkts_num_now > 0)
            temp_index = np.random.randint(0, pkts_num_now)
            add_index = 0
            stop_index = 0
            for j in range(self.flow_nums):
                add_index += flow_distribution_now[j]
                if add_index > temp_index:
                    stop_index = j
                    break
            pkt = self.flowid[stop_index]
            print(i, pkt)
            self.pkts_sequence.append(pkt)
            pkts_num_now -= 1
            flow_distribution_now[stop_index] -= 1


    def get_rand_flowid(self):
        lst = []
        for i in range(8):
            item = np.random.randint(1, 256)
            lst.append(str(item))
        srcip = ".".join(lst[0:4])
        dstip = ".".join(lst[4:8])
        proto = np.random.randint(1, 3)
        if 1 == proto:
            proto = "6"
        elif 2 == proto:
            proto = "17"
        srcport = str(np.random.randint(1, 65536))
        dstport = str(np.random.randint(1, 65536))
        temp = "\"" + srcip + "\t" + dstip + "\t" + proto + "\t" + srcport + "\t" + dstport + "\""
        return temp


if __name__ == "__main__":
    ge = flow_packets_generator(100, 1, 20/19)