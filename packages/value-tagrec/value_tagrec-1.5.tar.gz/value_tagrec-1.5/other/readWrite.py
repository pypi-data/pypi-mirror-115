#!/usr/bin/env python
# coding: utf-8
import json
import other.Word as Word
import os

current_dir = os.path.dirname(__file__)
RELATIONS_FILE = os.path.join(current_dir, '../data/relations.json')
WORDS_FILE = os.path.join(current_dir, '../data/words.json')
WORDSATTR_FILE = os.path.join(current_dir, '../data/wordsAttr.json')
tagsFile = os.path.join(current_dir, '../data/tags')

def getRelationsDic(file = None):
    if file == None:
        file = RELATIONS_FILE
    return read_json_1dict(file)

def getWordsDic(file = None):
    #读取Words.json，并每一个word转换为Word类,整个一个dict，key为word，value为Word类
    if file == None:
        file = WORDS_FILE
    wordsDic = {}
    for wordName, wordAttr in read_json_1dict(file).items():
        word = Word.Word(wordName, wordAttr["level"], wordAttr["wordID"],
                         word1level=wordAttr["word1level"], word2level=wordAttr["word2level"],
                         word3level=wordAttr["word3level"], word4level=wordAttr["word4level"],
                         baseIinterpretation=wordAttr["baseIinterpretation"],
                         synonym=wordAttr["synonym"], antonym=wordAttr["antonym"],
                         sentence=wordAttr["sentence"],
                         url=wordAttr["url"], source=wordAttr["source"],
                         docURLs=wordAttr["docURLs"], docs=wordAttr["docs"])
        wordsDic[wordName] = word
    return wordsDic
    #return read_json_1dict(WORDS_FILE)

def getWordsAttrDic(file = None):
    #读取WordsAttr.json，并每一个word转换为Word类,整个一个dict，key为word，value为Word类
    if file == None:
        file = WORDSATTR_FILE
    wordsDic = {}
    for wordName, wordAttr in read_json_1dict(file).items():
        word = Word.Word(wordName, wordID=wordAttr["wordID"],
                         baseIinterpretation=wordAttr["baseIinterpretation"],
                         synonym=wordAttr["synonym"], antonym=wordAttr["antonym"],
                         sentence=wordAttr["sentence"],
                         url=wordAttr["url"], source=wordAttr["source"],
                         docURLs=wordAttr["docURLs"], docs=wordAttr["docs"])
        wordsDic[wordName] = word
    return wordsDic

def write_json_1dict(dic, jsonFile):
    """
    一个dict写成json文件，一个可视化使用
    :param dic: 一个dict
    :param jsonFile: 路径
    :return:
    """
    with open(jsonFile, "w", encoding='utf-8') as w:
        #w.write(json.dumps(dic, ensure_ascii=False)+"\n")  # 写为一行
    #with open(jsonFile[:-5]+"_mulLine.json", "w", encoding='utf-8') as w:
        w.write(json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)+"\n")  # 写为多行

def read_json_1dict(path):
    """
    读取json，用于一个dict
    :param path: 路径，一个正常可读的多行json即可
    :return: 一个dict
    """
    with open(path, "r", encoding='utf-8') as r:
        dic = json.load(r)
    #print(dic)
    return dic

def readTXT(path):
    data = []
    with open(path, "r", encoding= 'utf-8') as r:
        for line in r.readlines():
            data.append(line.strip("\n"))
    return data

def writeTXT(data, path):
    with open(path, "w", encoding='utf-8') as w:
        for line in data:
            w.write(line+"\n")

def readTXT_1str(path):
    ###读成一个字符串，包括中间所有换行符
    with open(path, "r", encoding= 'utf-8') as r:
        data = r.read()
    return data

def writeTXT_1str(data, path):
    ###写一个字符串，包括中间所有换行符
    with open(path, "w", encoding='utf-8') as w:
        w.write(data)

def read_json(path):
    with open(path, "r", encoding='utf-8') as r:
        dics = [json.loads(line.strip()) for line in r.readlines()]
    #print(dics)
    return dics

def write_json_2format(dics, jsonFile):
    with open(jsonFile, "w", encoding='utf-8') as w:
        for dic in dics:
            w.write(json.dumps(dic, ensure_ascii=False)+"\n")  # 写为一行
    with open(jsonFile[:-5]+"_mulLine.json", "w", encoding='utf-8') as w:
        for dic in dics:
            w.write(json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False)+"\n")  # 写为多行

def read_json_1listDics(path):
    #读取json文件，格式为一个list，list中每个元素是一个dict,每个dict可多行显示，例如：
    '''
    [{
        "_id": "a",
        "title": "新年戏曲晚会在京举行",
        "date": "20200101",
        "url": "http://paper.people.com.cn/rmrb/html/2020-01/01/nw.D110000renmrb_20200101_6-03.htm",
        "pageName": "第03版：要闻",
        "md5": "a72f6bd1bcdfd83c6cdebc78eb6387a4",
        "processed": 0
    }, {
        "_id": "b",
        "title": "国家主席习近平发表二〇二〇年新年贺词",
        "date": "20200101",
        "url": "http://paper.people.com.cn/rmrb/html/2020-01/01/nw.D110000renmrb_20200101_2-01.htm",
        "pageName": "第01版：要闻",
        "md5": "802c9451d67b18b3c210d6a3fa8f55cf",
        "processed": 0
    }]
    '''
    with open(path, "r", encoding='utf-8') as f:
        strList = json.load(f)
    return strList

def readTagsFile(tagLevel):
    """
    从文件中读取标签，以及标签对应相似度比较字符串的value
    :param tagsFile: 文件部分路径，后加 _3level.json，_4level.json.
    :param tagLevel: 3或4级
    :return: tagsDic, key为标签，value为需要比较的字符串，空格拼接而成，3级为本身+四级s；4级为本身
    """
    if str(tagLevel) == '3':
        return read_json_1dict(tagsFile+"_3level.json")
    elif str(tagLevel) == '4':
        return read_json_1dict(tagsFile+"_4level.json")
    else:
        print("Only tagLevel 3 or 4 is allowed!")
        exit()
        return None