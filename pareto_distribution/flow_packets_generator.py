import numpy as np

class flow_packets_generator:
    def __init__(self, concurrency_flow_nums, pkts_num, min_num, alpha, save_file):
        self.concurrency_flow_nums = concurrency_flow_nums
        self.pkts_num = pkts_num
        self.min_num = min_num
        self.alpha = alpha
        self.save_file = save_file
        self.flow_distribution = np.floor((np.random.pareto(self.alpha, size=self.concurrency_flow_nums) + 1) * self.min_num).astype(int)
        for i in self.flow_distribution:
            assert(i > 0)
        self.flow_distribution_record = list(self.flow_distribution)
        self.flowid_record = []
        self.flowid = []
        for i in range(self.concurrency_flow_nums):
            tempid = self.get_rand_flowid()
            self.flowid.append(tempid)
            self.flowid_record.append(tempid)

        self.pkts_sequence = []
        self.get_pkts_sequence()

    def show_flow_distribution(self):
        sorted_distribution = np.sort(self.flow_distribution_record)
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
        pkts_num = sum(self.flow_distribution_record)
        print("实际生成的总数据包的数量为：", pkts_num)
        print("每个流的平均数据包量为：", pkts_num / len(self.flow_distribution_record))

    def get_pkts_sequence(self):
        pkts_num_now = sum(self.flow_distribution)
        with open(self.save_file,'w') as f:
            f.write("[")

            for i in range(self.pkts_num):
                if i % 1000000 == 0:
                    print("进度报告：", i / self.pkts_num)
                temp_index = np.random.randint(0, pkts_num_now)
                add_index = 0
                stop_index = 0
                for j in range(self.concurrency_flow_nums):
                    add_index += self.flow_distribution[j]
                    if add_index > temp_index:
                        stop_index = j
                        break
                if i != self.pkts_num - 1:
                    pkt = self.flowid[stop_index] + ","
                else:
                    pkt = self.flowid[stop_index]
                f.write(pkt)
                self.pkts_sequence.append(pkt)
                pkts_num_now -= 1
                self.flow_distribution[stop_index] -= 1
                if self.flow_distribution[stop_index] == 0:
                    new_flow_num = (np.floor((np.random.pareto(self.alpha, size=1) + 1) * self.min_num).astype(int))[0]
                    self.flow_distribution[stop_index] = new_flow_num
                    new_flow_id = self.get_rand_flowid()
                    self.flowid[stop_index] = new_flow_id
                    self.flowid_record.append(new_flow_id)
                    pkts_num_now += new_flow_num
            f.write("]")
            print("最终生成的总流个数：", len(self.flowid_record))
            print("平均每个流的数据包数量为：", len(self.flowid_record) / self.pkts_num)

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
    for i in range(1, 6):
        print("第", i, "次 trace 文件开始生成")
        filename = "trace" + str(i)
        ge = flow_packets_generator(100000, 20010000, 1, 1 + i * 0.05, filename)