#!/usr/bin/env python
# coding: utf-8
class Word:
    """
    用于帮助建立Words.json
    """
    name = ""
    level = -1 #该词属于第几层节点
    wordID = -1
    word1level = None
    word2level = None
    word3level = None
    word4level = None
    baseIinterpretation = None
    synonym = None#近义词
    antonym = None#反义词
    sentence = None#例句
    url = None#抽取近反义词新的的网页
    source = None#抽取近反义词信息网站的主页
    docURLs = None#种子文档对应的网页链接list
    docs = None#种子文档对应的download下来的文本dict，{序号：{见下}， 序号：{见下}}
    # docID:1,会在data/docs会存在一个1.txt的原始内容文档，和一个1_extract.txt抽取到的文档--int
    # docURL,爬取该文档的url: docID:url--""
    # docTitle:单独爬取出来的新闻标题--""
    # docSentences：抽取出的文档内容，按段划分，每篇文档一个list，包含标题+正文内容--[]
    # docCode：网页的编码方式--""

    def __init__(self, name, level=None, wordID=None,
                 word1level=None, word2level=None, word3level=None, word4level = None,
                 baseIinterpretation = None, synonym = None, antonym = None, sentence = None,
                 url=None, source = None, docURLs = None, docs=None):
        """
        初始化创建类
        """
        self.name = name
        self.level = level
        self.wordID = wordID
        self.word1level = word1level
        self.word2level = word2level
        self.word3level = word3level
        self.word4level = word4level
        self.baseIinterpretation = baseIinterpretation
        self.synonym = synonym
        self.antonym = antonym
        self.sentence = sentence
        self.url = url
        self.source = source
        self.docURLs = docURLs
        self.docs = docs


    def getFatherName(self):
        """
        获取当前节点的直接父节点Name
        :return:
        """
        if self.level == 1:
            return None
        elif self.level == 2:
            return self.word1level
        elif self.level == 3:
            return self.word2level
        elif self.level == 4:
            return self.word3level
        return None

    def getChildrensList(self):
        """
        获取当前节点的直接子节点list,
        注意，第四层节点的 子节点list为空
        :return:
        """
        if self.level == 1:
            return self.word2level
        elif self.level == 2:
            return self.word3level
        elif self.level == 3:
            return self.word4level
        elif self.level == 4:
            return None
        return None

    def printSynonym(self):
        """
        返回要打印格式的近义词列表
        :return:
        """
        if self.level != 4:
            return ""
        return '；'.join(self.synonym)

    def printAntonym(self):
        """
        返回要打印格式的反义词列表
        :return:
        """
        if self.level != 4:
            return ""
        return '；'.join(self.antonym)

    def printBaseIinterpretation(self):
        """
        返回要打印格式的基本释义
        :return:
        """
        if self.level != 4:
            return ""
        return ' '.join(self.baseIinterpretation)

    def printSentence(self):
        """
        返回要打印格式的例句
        :return:
        """
        if self.level != 4:
            return ""
        return ' '.join(self.sentence)

    def printDocURLs(self):
        """
        返回要打印格式的种子文档对应的urls，一个一行
        :return:
        """
        if self.level != 4:
            return ""
        return '\n'.join(self.docURLs)

    def printNameAndLevel(self):
        """
        返回要打印格式的name和level
        :return:
        """
        return self.name + "。位于知识图谱第" + str(self.level) + "层"

    def printFather(self):
        """
        返回要打印格式的father
        :return:
        """
        return "父节点：" + self.getFatherName()

    def printChildrens(self):
        """
        返回要打印格式的children
        :return:
        """
        return "子节点：" + '；'.join(self.getChildrensList())

    def printWordList(self):
        """
        输出该节点的所有信息
        :return: list形式
        """
        wordList = []
        wordList.append(self.printNameAndLevel())
        if self.level == 1:
            wordList.append(self.printChildrens())
        elif self.level == 2:
            wordList.append(self.printFather())
            wordList.append(self.printChildrens())
        elif self.level == 3:
            wordList.append("第一层节点" + self.word1level)
            wordList.append(self.printFather())
            wordList.append(self.printChildrens())
        elif self.level == 4:
            wordList.append("第一层节点" + self.word1level)
            wordList.append("第二层节点" + self.word2level)
            wordList.append(self.printFather())
            wordList.append("基本释义: " + self.printBaseIinterpretation())
            wordList.append("近义词: " + self.printSynonym())
            wordList.append("反义词: " + self.printAntonym())
            wordList.append("例句: " + self.printSentence())
            wordList.append("核心文档网址: \n" + self.printDocURLs())
        return wordList

    def printWord(self):
        """
        输出该节点。包括根->父节点->本身节点,用 / 分割，低等级在前，高等级在后
        :return:
        """
        if self.level == 1:
            return self.name
        if self.level == 2:
            return self.name + '/' + self.word1level
        if self.level == 3:
            return self.name + '/' + self.word2level + '/' + self.word1level
        if self.level == 4:
            return self.name+ '/' + self.word3level+ '/' + self.word2level + '/'+self.word1level
        return None

    def toDict(self):
        """
        将该节点转换为字典，不同level转换后需要的信息不同
        :return:
        """
        dic = {"name":self.name, "level":self.level, "wordID":self.wordID,
               "word1level":self.word1level, "word2level":self.word2level,
               "word3level":self.word3level, "word4level":self.word4level,
               "baseIinterpretation":self.baseIinterpretation, "synonym":self.synonym, "antonym":self.antonym,
               "sentence":self.sentence, "url":self.url, "source":self.source, "docURLs": self.docURLs,
               "docs":self.docs}
        return dic

    def toDictAttr(self):
        """
        将该节点转换为字典
        :return:
        """
        dic = {"name":self.name, "wordID":self.wordID,
               "baseIinterpretation":self.baseIinterpretation, "synonym":self.synonym, "antonym":self.antonym,
               "sentence":self.sentence, "url":self.url, "source":self.source, "docURLs": self.docURLs,
               "docs":self.docs}
        return dic

