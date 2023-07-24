import os.path
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import random

from config.config_utils import BASE_DIR
from tfidf.participle import DataParticiple

train_matrix_path = os.path.join(BASE_DIR, "train_features.pickle")
train_fit_path = os.path.join(BASE_DIR, "train_fit.pickle")


class TfidfExtract:

    def __init__(self, file_name):
        self.file_name = file_name
        self.random_number = 0
        self.train_data_list = None
        self.participle = DataParticiple(file_name)

    def train_model(self, search_text=None):
        # 停用词集合
        stopword_path = os.path.join(BASE_DIR, "tfidf", 'stopwords.txt')
        stopword_list = [k.strip() for k in open(stopword_path, encoding='utf8').readlines() if k.strip() != '']
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w\w+\b", use_idf=1,
                                     stop_words=stopword_list)
        # 判断文件是否存在，不存在的话就进行分词操作
        if os.path.exists(train_matrix_path) is False:
            start = time.time()
            self.train_data_list = self.participle.data_participle()
            end = time.time()
            print(f"分词成功,所用时间为：{end - start}")
        # 判断fit文件是否存在，存在的话就直接读取
        if os.path.exists(train_fit_path):
            train_fit = pickle.load(open(train_fit_path, 'rb'))
        else:  # 不存在的话就创建
            train_fit = vectorizer.fit(self.train_data_list)
            pickle.dump(train_fit, open(train_fit_path, 'wb'))
        search_text_list = self.participle.keyword_participle(
            self.random_extract_text(self.file_name) if search_text is None else search_text)  # 将要查找的文本内容进行分词
        if os.path.exists(train_matrix_path):  # 判断这个路径是否存在,存在的话就加载
            train_matrix = pickle.load(open(train_matrix_path, "rb"))
        else:  # 不存在的会创建
            train_matrix = vectorizer.transform(self.train_data_list)
        test_matrix = train_fit.transform(search_text_list)
        # 求余弦相似度
        similarity = cosine_similarity(train_matrix, test_matrix)
        similarity = similarity.ravel().argsort()[::-1][0:10]
        # print(similarity)
        # 判断文件是否存在，不存在的话就进行写入操作
        if os.path.exists(train_matrix_path) is False:
            pickle.dump(train_matrix, open(train_matrix_path, "wb"))
        return similarity  # 返回排序后的索引

    def random_extract_text(self, filename):
        """
        随机抽取一篇文章中的一部分进行测试
        :param filename:
        :return:返回获取到的文章内容
        """
        with(open(os.path.join(BASE_DIR, filename), "r", encoding="UTF-8")) as f:
            # 1到100之间的随机数
            datas = f.readlines()
            self.random_number = random.randint(1, len(datas) - 1)  # 生成随机数
            print(self.random_number)
            print(eval(datas[self.random_number])["accusation"])
            return eval(datas[self.random_number])["fullText"][0:50]  # 随机获取文章内容

    def train_result(self, search_text=None):
        datas_list = []
        index = self.train_model(search_text)
        data_list = self.participle.get_content()
        for i in index:
            datas_list.append(data_list[i])
            print(data_list[i])
            print(data_list[i]['accusation'])

    def run_model(self, search_text):  # 这边是正式运行模块
        """
        此方法是使用训练好的模型
        :param search_text:
        :return:
        """
        train_fit = pickle.load(open(train_fit_path, 'rb'))
        train_matrix = pickle.load(open(train_matrix_path, "rb"))
        search_text_list = self.participle.keyword_participle(search_text)  # 要查找的文本内容
        test_matrix = train_fit.transform(search_text_list)
        # 求余弦相似度
        similarity = cosine_similarity(train_matrix, test_matrix)
        similarity = similarity.ravel().argsort()[-5:][::-1]  # 选择相似度最高的5个
        return similarity  # 返回排序后的索引

    def select_result(self, search_text):
        datas_list = []
        index = self.run_model(search_text)
        data_list = self.participle.get_content()
        for i in index:
            # print(data_list[i])
            datas_list.append(data_list[i])
        return datas_list


if __name__ == '__main__':
    # file_name = "../data.json"
    begin = time.time()
    tf_idf = TfidfExtract("data.json")
    # tf_idf.train_result("欺骗")
    # tf_idf.train_result("诈骗罪")
    # tf_idf.train_result("诈骗罪上海市")
    # tf_idf.train_result("曾因犯诈骗罪")
    # tf_idf.train_result("其行为已构成诈骗罪")
    # tf_idf.train_result("诈骗他人财物，数额较大的犯罪事实")
    # tf_idf.train_result("实施电信网络诈骗犯罪而组成较为固定的犯罪组织，依法应认定为诈骗犯罪集团")
    # tf_idf.train_result("以投注“时时彩”的方式在“鼎盛娱乐”诈骗平台注册充值，再在后台以虚假中奖信息、以及扮演客服答复提现障碍等方式诱骗被害人继续充值")
    end = time.time()
    print(f"运行所用时间：{end - begin}")
    # tf_idf.train_result("盗窃罪")
    # tf_idf.train_result("盗窃罪北京市")
    # tf_idf.train_result("曾因犯盗窃罪于2016年12月被判处拘役四个月")
    # tf_idf.train_result("因犯盗窃罪被判处有期徒刑一年")
    # tf_idf.train_result("曾因犯盗窃罪于2016年12月被判处拘役四个月")
    # tf_idf.train_result("现因涉嫌犯盗窃罪于2019年1月5日被刑事拘留，同年2月2日被逮捕。")
    # tf_idf.train_result("再因涉嫌盗窃犯罪，于2019年3月19日被刑事拘留，同年3月27日被逮捕")
    # tf_idf.train_result("因盗窃被劳动教养一年六个月。2011年4月12日因犯盗窃罪被判处有期徒刑八个月，并处罚金人民币一千元")
    # tf_idf.train_result("走私")
    # tf_idf.train_result("制造毒品")
    # tf_idf.train_result("走私、贩卖、运输、制造毒品罪")
    # tf_idf.train_result("走私、贩卖、运输、制造毒品上海市")
    # tf_idf.train_result("被告人XXX明知是毒品甲基苯丙胺仍予以非法销售，合计2.49克")
    # tf_idf.train_result("被告人明知是毒品而贩卖，其行为已构成贩卖毒品罪")
    # tf_idf.train_result("扣押物品照片、毒品称量录像及照片")
    # tf_idf.train_result("公安机关的扣押决定书、扣押清单、称量笔录、清点笔录、毒品检验报告、收缴毒品专用单据、案发及抓获经过")
    # tf_idf.train_result("违反国家毒品管理法规，向他人贩卖毒品甲基苯丙胺，其行为已构成贩卖毒品罪")
    # tf_idf.train_result("在本市杨浦区通北路XXX号门口将2粒俗称“蓝精灵”的淡蓝色药片贩卖给购毒人员史某某，交易完成后被民警当场人赃俱获。经上海市毒品检验中心检验")
    # tf_idf.train_result("危险驾驶罪")
    # tf_idf.train_result("危险驾驶罪宝山区")
    # tf_idf.train_result("醉酒驾驶")
    # tf_idf.train_result("因违章停车被民警查获。经鉴定，杨某某血液中乙醇含量为1.24mg/ml，属醉酒驾驶")
    # tf_idf.train_result("且有血样提取登记表、呼吸式酒精测试单")
    # tf_idf.train_result("被告人饮酒后无驾驶资格驾驶一辆小型轿车途经上海市青浦区沪青平公路进青松路西约100米处时")
    # tf_idf.train_result("犯危险驾驶罪的事实清楚，证据确实、充分，指控罪名成立，量刑建议适当，应予采纳")
    # tf_idf.train_result("危险驾驶一审刑事判决书")
    # tf_idf.train_result("随后执勤民警将其带至医院抽取血样。经广东中一司法鉴定中心鉴定，被告人朱某某血液中检出乙醇")
    # tf_idf.train_result("在上前处置时发现被告人坐在正驾驶位置睡觉，遂予以叫醒，在双方对话过程中，民警发现被告人陈某某身上有酒味")
    # tf_idf.train_result("寻衅滋事")
    # tf_idf.train_result("寻衅滋事罪北京市")
    # tf_idf.train_result("因涉嫌犯寻衅滋事罪被刑事拘留")
    # tf_idf.train_result("因涉嫌妨害公务、寻衅滋事")
    # tf_idf.train_result("酒后无故滋事，采用掌刮、踢踹等方式对正在作业的环卫工人进行殴打")
    # tf_idf.train_result("持砖头任意损毁被害人停放于此的小型普通客车。")
    # tf_idf.train_result("醉酒后因买单费用与他人发生口角，为逞强斗狠，采用酒瓶打砸的方式，无故砸毁桌面玻璃一块")
    # tf_idf.train_result("被告人刘某某曾因犯寻衅滋事罪受过刑事处罚，又随意殴打他人，致一人轻微伤，情节恶劣")
    # tf_idf.train_result("被告人在东北烧烤店内，与隔壁桌用餐的被告人酒后因琐事发生纠纷，互相推搡，后被人劝开，但仍骂骂咧咧，后被告人为泄愤用餐具砸向对方，致受伤，")
    # tf_idf.train_result("被害人左侧鼻骨粉碎性骨折，构成轻伤，左眼挫伤，构成轻微伤")

