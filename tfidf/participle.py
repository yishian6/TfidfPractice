import jieba
import json
import os
import re
import time
from multiprocessing import Process, Queue

from config.config_utils import BASE_DIR
from tfidf.data_handle import Participle


class DataParticiple(Participle):

    def __init__(self, file_name):
        self.content = []
        # 将json文件打开并转化为字符串的形式

        # 对列表进行切片
        self.participle_length = 0
        self.dataSet_1 = []
        self.dataSet_2 = []
        self.dataSet_3 = []
        self.dataSet_4 = []
        self.dataSet_5 = []
        self.dataSet_6 = []
        self.dataSet_7 = []
        self.dataSet_8 = []
        with open(os.path.join(BASE_DIR, file_name), 'r', encoding='utf-8') as f:
            # 逐行将数据加入列表
            for line in f:
                # 将str类数据转换城字典类
                json_data = json.loads(line)
                self.content.append(json_data)

    def data_partition(self):
        self.participle_length = int(len(self.content) / 8)
        self.dataSet_1 = self.content[0:self.participle_length]
        self.dataSet_2 = self.content[self.participle_length:2 * self.participle_length]
        self.dataSet_3 = self.content[2 * self.participle_length:3 * self.participle_length]
        self.dataSet_4 = self.content[3 * self.participle_length:4 * self.participle_length]
        self.dataSet_5 = self.content[4 * self.participle_length:5 * self.participle_length]
        self.dataSet_6 = self.content[5 * self.participle_length:6 * self.participle_length]
        self.dataSet_7 = self.content[6 * self.participle_length:7 * self.participle_length]
        self.dataSet_8 = self.content[7 * self.participle_length:len(self.content)]

    def process(self, content, q):
        message = []
        for i in range(self.participle_length):
            for k, v in content[i].items():
                if k == 'fullText':
                    text = re.sub(r"[^\u4e00-\u9fa5 ]+", '', v)
                    message.append(' '.join(list(jieba.cut(text))))
                    # print(' '.join(list(jieba.cut(v))))
        q.put(message)
        print("one done")

    def data_participle(self):
        self.data_partition()
        time_start = time.time()
        # p = Pool(8)
        q = Queue()
        # p.apply_async(self.process_1, (q,))
        # p.apply_async(self.process_2, (q,))
        # p.apply_async(self.process_3, (q,))
        # p.apply_async(self.process_4, (q,))
        # p.apply_async(self.process_5, (q,))
        # p.apply_async(self.process_6, (q,))
        # p.apply_async(self.process_7, (q,))
        # p.apply_async(self.process_8, (q,))
        # 创建进程
        t1 = Process(target=self.process, args=(self.dataSet_1, q))
        t2 = Process(target=self.process, args=(self.dataSet_2, q))
        t3 = Process(target=self.process, args=(self.dataSet_3, q))
        t4 = Process(target=self.process, args=(self.dataSet_4, q))
        t5 = Process(target=self.process, args=(self.dataSet_5, q))
        t6 = Process(target=self.process, args=(self.dataSet_6, q))
        t7 = Process(target=self.process, args=(self.dataSet_7, q))
        t8 = Process(target=self.process, args=(self.dataSet_8, q))
        # p.close()
        # p.join()

        # 开始进程
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()

        # 获取数据
        res1 = q.get()
        res2 = q.get()
        res3 = q.get()
        res4 = q.get()
        res5 = q.get()
        res6 = q.get()
        res7 = q.get()
        res8 = q.get()

        # 等待线程全部结束

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        # p.terminate()
        participle_set = res1 + res2 + res3 + res4 + res5 + res6 + res7 + res8
        time_end = time.time()
        time_c = time_end - time_start  # 运行所花时间
        print('time cost', time_c, 's')
        return participle_set

    def keyword_participle(self, search_text):  # 进行关键词的分词操作
        data_list = []
        text = re.sub(r"[^\u4e00-\u9fa5 ]+", ' ', search_text)
        data_list.append(" ".join(jieba.lcut(text)))
        return data_list

    def get_content(self):
        return self.content


if __name__ == '__main__':
    a = DataParticiple("data.json")
    print(a.data_participle())
