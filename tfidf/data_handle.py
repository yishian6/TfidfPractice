from abc import ABC, abstractmethod


class Participle(ABC):

    @abstractmethod
    def data_participle(self):
        """
        以列表的形式返回分好的词
        :param :
        :return: 
        """
        pass

    @abstractmethod
    def keyword_participle(self, search_text):
        pass

    @abstractmethod
    def get_content(self):
        pass
