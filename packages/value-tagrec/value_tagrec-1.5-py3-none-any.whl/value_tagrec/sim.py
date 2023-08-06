#!/usr/bin/env python
# coding: utf-8
###通过计算标签与文本的相似度，提供标签和置信度；同时，针对文本的不同部分，给出不同权重（标题、首段、末段给予不同权重；近反义词；基本释义等也计算相似度给出不同权重）
import other.sim_sentence as sim_sentence #sim_sentence.calSimSentence(s1, s2, 'levenshtein')
import other.readWrite as readWrite
import time
from terminaltables import AsciiTable
simMethod = 'levenshtein'

def dealText(textStr):
    """
    处理文本篇章字符串。分为标题、首段、中间段、尾段，原字符串仍保留。划分后部分去掉空行
    据其句子长度、句前是否空格、段之间空行个数
    :param textStr: 文本篇章字符串
    :return: 字典{"str":textStr, "title":, "firstParagraph":"", "lastParagraph":"", "midParagraph":""}
    """
    def numSpace_atBeginOFS(s):
        """
        计算字符串首，即段首，空格个数，一个 \t 记为4个空格
        :param s: 字符串
        :return: 个数
        """
        s = s.replace('\t', '    ')#\t转换
        sLStrip = s.lstrip()  # 去掉最左侧空格
        num = len(s) - len(sLStrip)
        return num

    textDic = {"str":textStr}
    textList = textStr.split('\n')
    if not textList:
        return None
    # 去掉最后一行的（新华社北京1月8日电）。形式，否则影响尾段的判断
    line = textList[-1].strip()#去掉前后空格
    if line and line[0]=="（" and line[-1] == "）":
        textList.pop()

    #根据段间空行划分
    spaceSegFlag = 0
    countPara = 0
    oldCountPara = 0
    lineI = 0
    newTextList = []#无空行文本
    for line in textList:
        if line == "":
            countPara += 1
            continue
        else:
            lineI += 1
            newTextList.append(line)
            if lineI == 1:
                countPara = 0
            elif lineI == 2:
                oldCountPara = countPara
                countPara = 0
            elif lineI == 3:
                if countPara < oldCountPara and len(line)<=50:#标题与第一段的空格行数 > 第一段与第二段间空格行数
                    ###成功
                    spaceSegFlag = 1
    if not newTextList:
        return None
    #当段落为0,1,2时，不划分了，全作为midParagraph
    if len(newTextList) < 3:#此时不作区分了
        textDic["title"] = ""
        textDic["firstParagraph"] = ""
        textDic["lastParagraph"] = ""
        textDic["midParagraph"] = '\n'.join(newTextList)
        return textDic
    if spaceSegFlag:#根据段间空行划分  成功
        textDic["title"] = newTextList[0]
        textDic["firstParagraph"] = newTextList[1]
        textDic["lastParagraph"] = newTextList[-1]
        textDic["midParagraph"] = '\n'.join(newTextList[2:-1])
        return textDic

    #空格划分方法失败；未找到标题。。使用每段前面空格划分--找标题
    numSpaceline0 = numSpace_atBeginOFS(newTextList[0])
    numSpaceline1 = numSpace_atBeginOFS(newTextList[1])
    numSpaceline2 = numSpace_atBeginOFS(newTextList[2])
    if len(newTextList[0])<=50 and numSpaceline0 != numSpaceline1 and numSpaceline1 == numSpaceline2:
        textDic["title"] = newTextList[0]
        textDic["firstParagraph"] = newTextList[1]
        textDic["lastParagraph"] = newTextList[-1]
        textDic["midParagraph"] = '\n'.join(newTextList[2:-1])
        return textDic

    #还有一种划分失败情况，空格和段落均无法划分，但正文会重复一遍标题内容.此时不考虑标题长度了
    if newTextList[0].lstrip() == newTextList[1].lstrip():
        textDic["title"] = newTextList[0]
        textDic["firstParagraph"] = newTextList[1]
        textDic["lastParagraph"] = newTextList[-1]
        textDic["midParagraph"] = '\n'.join(newTextList[2:-1])
        return textDic

    #最后情况，无法划分出标题
    textDic["title"] = ""
    textDic["firstParagraph"] = newTextList[0]
    textDic["lastParagraph"] = newTextList[-1]
    textDic["midParagraph"] = '\n'.join(newTextList[1:-1])
    return textDic


def tagRec_sim(wordsAttrDic, textDic, tagsDic, tagLevel, top, confidenceLowerBound):
    """
    为文本篇章贴标签，返回，符合要求的qiantop个标签，及其置信度
    :param wordsAttrDic 核心词属性文件
    :param textDic: 文本字典，已经划分为{"str":textStr, "title":, "firstParagraph":"", "lastParagraph":"", "midParagraph":""}，计算相似度时给予不同权重
    :param tagsDic: 标签，key为标签，value为需要比较的字符串，空格拼接而成，3级为本身+四级s；4级为本身
    :param tagLevel: 要给出的标签属于几级，默认为3
    :param top: 选取置信度前top的标签，默认为5
    :param confidenceLowerBound: #取置信度 >= 该值的标签。。默认为0
    :return: tagsRec 返回的标签推荐，以及置信度。按置信度倒序，每个元素为（tag, 置信度）
    """
    # 直接计算完整字符串和标签的相似度，乘以一个rate，作为置信度
    # textLen = len(textDic["str"])
    # tagLen = 20
    # rate = textLen/(tagLen * 7)#将置信度乘以一个比例，根据句子长度，调整一下值
    # for tag, value in tagsDic.items():
    #     allResults[tag] = sim_sentence.calSimSentence(textDic["str"], value, simMethod)*rate

    tagsRec = []
    allResults = {}
    titleWeight = 1.2
    firstParaWeight = 1
    minParaWeight = 0.8
    #attrWeight = 0.2 #标签属性信息权重
    textLen = len(textDic["str"])#整个文本长度
    for tag, value in tagsDic.items():
        allResults[tag] = sim_sentence.calSimSentence(textDic["title"], value, simMethod) * titleWeight + \
                        sim_sentence.calSimSentence(textDic["firstParagraph"], value, simMethod) * firstParaWeight + \
                        sim_sentence.calSimSentence(textDic["lastParagraph"], value, simMethod) * firstParaWeight + \
                        sim_sentence.calSimSentence(textDic["midParagraph"], value, simMethod) * minParaWeight
        # 考虑标签的所有属性信息，作为相似度，乘以一个小的比例，直接加到上面相似度结果中
        # word3or4level = tag.split('_')[0]
        # synonymValue = 0.0 if not wordsAttrDic[word3or4level].synonym else sim_sentence.calSimSentence('_'.join(wordsAttrDic[word3or4level].synonym), textDic["str"], 'levenshtein')
        # antonymValue = 0.0 if not wordsAttrDic[word3or4level].antonym else sim_sentence.calSimSentence('_'.join(wordsAttrDic[word3or4level].antonym), textDic["str"], 'levenshtein')
        # sentenceValue = 0.0 if not wordsAttrDic[word3or4level].sentence else sim_sentence.calSimSentence('_'.join(wordsAttrDic[word3or4level].sentence), textDic["str"], 'levenshtein')
        # baseIinterpretationValue = 0.0 if not wordsAttrDic[word3or4level].baseIinterpretation else sim_sentence.calSimSentence('_'.join(wordsAttrDic[word3or4level].baseIinterpretation), textDic["str"], 'levenshtein')
        # print(tag + "\t近义词：" + str(synonymValue) + "\t反义词：" + str(antonymValue) + "\t例句：" + str(
        #     sentenceValue) + "\t基本释义：" + str(baseIinterpretationValue))
        # allResults[tag] += (synonymValue + antonymValue + sentenceValue + baseIinterpretationValue) * attrWeight
        #对最后的结果乘一个比例值，根据文本长度，看乘以多少
        y = 0.29*textLen + 76
        rate = textLen/(y)#将置信度乘以一个比例，根据句子长度，调整一下值
        allResults[tag] *= rate
    #print(textLen)

    #排序以及取前top，根据置信度下界，得到返回值
    sortAllResults = sorted(allResults.items(), key=lambda item: item[1], reverse=True)  # 根据相似度逆序排序
    for i in range(top):  # 取前top个
        if sortAllResults[i][1] > 0.99 and confidenceLowerBound<=0.99:#防止结果大于1
            tagsRec.append((sortAllResults[i][0], 0.99))
            continue
        if sortAllResults[i][1] < confidenceLowerBound:
            break
        tagsRec.append(sortAllResults[i])

    #输出结果标签，以及计算的所有权重
    # for tag, con in tagsRec:
    #     print(tag+"-- title:"+str(sim_sentence.calSimSentence(textDic["title"], tagsDic[tag], simMethod) * titleWeight) + \
    #           "\tfirstPara:"+str(sim_sentence.calSimSentence(textDic["firstParagraph"], tagsDic[tag], simMethod) * firstParaWeight) + \
    #           "\tlastPara:"+str(sim_sentence.calSimSentence(textDic["lastParagraph"], tagsDic[tag], simMethod) * firstParaWeight) + \
    #           "\tmidPara:"+str(sim_sentence.calSimSentence(textDic["midParagraph"], tagsDic[tag], simMethod) * minParaWeight)+ \
    #           "\tresult:"+str(con) + \
    #           "\tfullStrCompare: "+str(sim_sentence.calSimSentence(textDic["str"], tagsDic[tag], simMethod)))
    # print()

    #把直接计算字符串的结果输出比较。不考虑划分权重
    # listtt = ["民主_社会主义先进文化_国家", "民主_五四精神_中国精神", "以人为本_抗震救灾精神_中国精神"]
    # for tag in listtt:
    #     t = sim_sentence.calSimSentence(textDic["title"], tagsDic[tag], simMethod)
    #     f = sim_sentence.calSimSentence(textDic["firstParagraph"], tagsDic[tag], simMethod)
    #     l = sim_sentence.calSimSentence(textDic["lastParagraph"], tagsDic[tag], simMethod)
    #     m = sim_sentence.calSimSentence(textDic["midParagraph"], tagsDic[tag], simMethod)
    #     con = t * titleWeight + f * firstParaWeight + l * firstParaWeight + m * minParaWeight
    #     print(tag + "-- title:" + str(t * titleWeight) + "\tfirstPara:" + str(f * firstParaWeight) + "\tlastPara:" + str(
    #         l * firstParaWeight) + "\tmidPara:" + str(m * minParaWeight) + "\tresult:" + str(con)+ \
    #           "\tfullStrCompare: "+str(sim_sentence.calSimSentence(textDic["str"], tagsDic[tag], simMethod)))
    # print()
    return tagsRec


def writeTagsFile(tagsFile):
    """
    将标签提前写入文件，3级和4级标签
    :param tagsFile: 文件部分路径，后加 _3level.json，_4level.json.
            key为标签，value为需要比较的字符串，空格拼接而成，3级为本身+四级s；4级为本身
    :return: None，直接写入json文件
    """
    relationsDic = readWrite.getRelationsDic()
    #3级
    tagsDic = {}
    for word1level, word2levels in relationsDic.items():
        for word2level, word3levels in word2levels.items():
            for word3level, word4levels in word3levels.items():
                join123 = word3level + '_' + word2level + '_' + word1level
                tagsDic[join123] = [word1level, word2level, word3level]
                tagsDic[join123].extend(word4levels)
                tagsDic[join123] = ' '.join(tagsDic[join123])
    readWrite.write_json_1dict(tagsDic, tagsFile+"_3level.json")
    # 4级
    tagsDic = {}
    for word1level, word2levels in relationsDic.items():
        for word2level, word3levels in word2levels.items():
            for word3level, word4levels in word3levels.items():
                for word4level in word4levels:
                    join1234 = word4level + '_' + word3level + '_' + word2level + '_' + word1level
                    tagsDic[join1234] = [word1level, word2level, word3level, word4level]
                    tagsDic[join1234] = ' '.join(tagsDic[join1234])
    readWrite.write_json_1dict(tagsDic, tagsFile + "_4level.json")

def execute(textStr, tagLevel, top, confidenceLowerBound):
    """
    执行主函数，输入文本以及要求限制，输出label+置信度
    :param textStr: 输入文本，字符串
    :param tagLevel:最终标注为几级标签，默认为3
    :param top:最终标签取前几个，默认为5
    :param confidenceLowerBound:取置信度 >= 该值的标签，默认为0
    :return: None
    """
    #start = time.time()
    # textFile = "../texts/1.txt"
    # textStr = '\n'.join(readWrite.readTXT(textFile))
    textDic = dealText(textStr)
    if textDic == None:  # 输入为空文本
        print("输入为空文本！")
        exit()
    # readWrite.write_json_1dict(textDic, "texts/1.json")#将处理后的文件写入json
    #tagsFile = "../data/tags"  # 标签文件所在的路径，分为3级和4级文件，根据taglevel读取
    #tagsFile = "../data/tags"
    # writeTagsFile(tagsFile)  将标签提前写入文件，3级和4级标签。。标签推荐应用时注释掉
    tagsDic = readWrite.readTagsFile(tagLevel)
    wordsAttrDic = readWrite.getWordsAttrDic()
    tagsRec = tagRec_sim(wordsAttrDic, textDic, tagsDic, tagLevel, top, confidenceLowerBound)
    #end = time.time()
    #结果打印输出
    printTags(tagLevel, tagsRec)
    # for key, value in tagsRec:
    #     print(key + ": " + str(value))
    #end = time.time()
    #print("所用时间：" + str(end - start))
    return tagsRec

def printTags(tagLevel, tagsRec):
    """
    将结果标签+置信度输出到控制台
    :param tagLevel:输出为几级标签
    :param tagsRec: 结果，一个list，每个元素是一个元祖（标签，置信度）
    :return: None
    """
    if tagLevel == 3:
        table_data = [['序号', '三级标签', '二级类别', '一级类别', '置信度']]
    else:
        table_data = [['序号', '四级标签', '三级类别', '二级类别', '一级类别', '置信度']]
    for i, (key, value) in enumerate(tagsRec):
        listt = [i]
        listt.extend(key.split('_'))
        listt.append(value)
        table_data.append(listt)
    table = AsciiTable(table_data)
    print(table.table)

if __name__ == '__main__':
    print("tagRecommendation/sim.py")
    textFile = "../texts/1.txt"
    textStr = '\n'.join(readWrite.readTXT(textFile))
    execute(textStr, tagLevel=3, top=5, confidenceLowerBound=0)
    ##非utf-8编码的，其他符号；；；；其他系统mac、linux的空行处理