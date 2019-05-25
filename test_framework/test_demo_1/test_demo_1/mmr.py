#coding=utf-8
import re
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
import os
import pymysql

# dbd = pymysql.connect(host='47.100.163.195', user='recommend', password='recommend', database='test', port=3306)
# # 使用cursor()方法创建一个游标对象cursor
# cursord = dbd.cursor()
# # 删除
# sqld = "DELETE FROM News Where length(content)<100;"
# try:
#     # 执行sql语句
#     cursord.execute(sqld)
#     # 提交到数据库
#     dbd.commit()
#     print('success')
# except:
#     # 如果出错执行回滚
#     dbd.rollback()
#     print('failed')
# dbd.close()

# dbg = pymysql.connect(host='47.100.163.195', user='recommend', password='recommend', database='test', port=3306)
# # 使用cursor()方法创建一个游标对象cursor
# cursorg = dbg.cursor()
# # 查询
# sqlg = "SELECT newsid,content FROM News where abstract is null;"
# try:
#     # 执行sql语句
#     cursorg.execute(sqlg)
#         # 通过fetchall获取results对象并打印结果
#     resultss = cursorg.fetchall()
#     print('success')
# except:
#     print('failed')
# delist = []
# for deleteem in resultss:
#     newid = deleteem[0]
#     contentem = deleteem[1]
#     if contentem:
#         deem = 0
#         wwfc = ['首先', '其次', '此外', '第一', '第二',  '', '']
#         for wwc in wwfc:
#             if wwc in contentem:
#                 deem = deem + 1
#         if deem > 3:
#             delist.append(newid)
# sqlf = "DELETE FROM News Where newsid = %s;"
# try:
#     # 执行sql语句
#     cursorg.execute(sqlf, (delist))
#     # 提交到数据库
#     dbg.commit()
#     print('success')
# except:
#     # 如果出错执行回滚
#     dbg.rollback()
#     print('failed')
# dbg.close()

f =open (r"C:\AllDoc\Github_Root\InternShip\test_framework\test_demo_1\test_demo_1\textrank4zh\stopwords.txt", encoding='utf-8')#导入停止词
stopwords = f.readlines()
stopdict = {}
for i in stopwords:
    stopdict[i.replace("\n", "")] = 0
stopwords = stopdict


def getAbstract(textsss):
    def cleanData(name):
        setlast = jieba.lcut(name, cut_all=False)
        seg_list = [i.lower() for i in setlast if i not in stopwords]
        return " ".join(seg_list)


    def calculateSimilarity(sentence, doc):  # 根据句子和句子，句子和文档的余弦相似度
        if doc == []:
            return 0
        vocab = {}
        for word in sentence.split():
            vocab[word] = 0  # 生成所在句子的单词字典，值为0

        docInOneSentence = '';
        for t in doc:
            docInOneSentence += (t + ' ')  # 所有剩余句子合并
            for word in t.split():
                vocab[word] = 0  # 所有剩余句子的单词字典，值为0

        cv = CountVectorizer(vocabulary=vocab.keys())
        docVector = cv.fit_transform([docInOneSentence])
        sentenceVector = cv.fit_transform([sentence])
        return cosine_similarity(docVector, sentenceVector)[0][0]

    data = textsss
    # print(len(data))
    sentenceString = ''

    hassentences = ''
    hasummary = []
    # if len(data) > 300:
    #     # duanluo = data.lstrip('**').split('**')  # 段落拆分
    #     duanluo = data.replace('**', '').split('。')  # 句子拆分
    #     for duan in duanluo:
    #         if len(hassentences) + len(duan) < 100:
    #             hassentences = hassentences + duan
    #             hasummary.append(cleanData(duan))
    #         else:
    #             break
        # hassummary = hassentences.replace('**', '').split('。')  # 句子拆分
        # hasummary = []
        # for hsummary in hassummary:
        #     hasummary.append(cleanData(hsummary))
        # if len(hassentences) > 300:
        #     hasummary = []
        # print(hasummary)
        # hasummary = list(set(hasummary))
        # hasummary.sort(key=hasummary.index)


    def sent_tokenizer(texts):
        start = 0
        i = 0  # 每个字符的位置
        sentences = []
        punt_list = ' !?】。！？'  # ',.!?:;~，。！？：；～'.decode('utf8')
        texts = texts.rstrip('*')
        for text in texts:
            if text in punt_list:  # 检查标点符号下一个字符是否还是标点
                sentences.append(texts[start:i + 1])  # 当前标点符号位置
                start = i + 1  # start标记到下一句的开头
                i += 1
            else:
                i += 1  # 若不是标点符号，则字符位置继续前移
        if start < len(texts):
            sentences.append(texts[start:])  # 这是为了处理文本末尾没有标点符号的情况
        return sentences
    listcleans = []
    listclean = []
    cleantexts = data.split('**')
    for cleantext in cleantexts:
        texts = cleantext.replace('*', '').replace('”', '')
        listcleans.extend((sent_tokenizer(texts)))
    # for nnjj in listcleans:
    #     print(nnjj)
    listclean = list(set(listcleans))
    listclean.sort(key=listcleans.index)
    # print(len(listcleans))
    # print(len(listclean))
    text = ''
    originalSentenceOf = {}
    for dfgh in listclean:
        text = text + dfgh
    print(len(text))
    print('\n')
    if len(text) > 300:
        # duanluo = data.lstrip('**').split('**')  # 段落拆分
        duanluo = text.replace('**', '').split('。')  # 句子拆分
        for duan in duanluo:
            if len(hassentences) + len(duan) < 100:
                hassentences = hassentences + duan
                cll = cleanData(duan)
                originalSentenceOf[cll] = duan
                hasummary.append(cll)
            else:
                break
    sentences = []
    clean = []
    # text = data.replace('**', '')
    # Data cleansing
    parts = text.split('。')  # 句子拆分
    # for ass in parts:
    #     print(ass)
    #   print (parts)
    for part in parts:
        part = re.sub(r'^\s+$', '', part)
        if part == '':
            continue
        cl = cleanData(part)  # 句子切分以及去掉停止词
        sentences.append(part)  # 原本的句子
        clean.append(cl)  # 干净有重复的句子
        originalSentenceOf[cl] = part  # 字典格式
    # 干净无重复的句子
    # for sdfsd in clean:
    #     print(sdfsd)
    # for ooii in clean:
    #     print(ooii)
    # print('\n')
    setClean = set(clean)
    scores = {}
    for data in clean:
        temp_doc = setClean - set([data])  # 在除了当前句子的剩余所有句子
        score = calculateSimilarity(data, list(temp_doc))  # 计算当前句子与剩余所有句子的相似度
        scores[data] = score  # 得到相似度的列表
    if len(text) > 450:
        n = 25 * len(sentences) / 100  # 摘要的比例大小
        alpha = 0.6
        summarySet = hasummary
        sentencecontent = ''
        # while n > 0:
        while len(hassentences) + len(sentencecontent) < 400:
            mmr = {}
            # kurangkan dengan set summary
            for sentence in scores.keys():
                # print(calculateSimilarity(sentence, summarySet))
                if not sentence in summarySet:
                    mmr[sentence] = alpha * scores[sentence] - (1 - alpha) * calculateSimilarity(sentence,
                                                                                                 summarySet)  # 公式
            try:
                selected = max(mmr.items(), key=operator.itemgetter(1))[0]
            except:
                break
            sentencecontent = sentencecontent + selected.replace(' ', '')
            if len(hassentences) + len(sentencecontent) < 400:
                # print(selected)
                summarySet.append(selected)
            else:
                break
            # n -= 1
        # xulie = []
        # for sdfsd in summarySet:
        #     print(sdfsd)
        if '' in summarySet:
            summarySet.remove('')
        summarySet = list(set(summarySet))
        summarySet.sort(key=clean.index)
        # print('\n')
        for summ in summarySet:
            # print(summ.replace(' ', ''))
            sentenceString = sentenceString + originalSentenceOf[summ] + '。'
        # print('\n')
        print(len(sentenceString))
    else:
        # print(data.replace('**', ''))
        sentenceString = text
        print(len(sentenceString))
    def cleansent_tokenizer(texts):
        start = 0
        i = 0  # 每个字符的位置
        sentences = []
        punt_list = ' !?）)】。！？'  # ',.!?:;~，。！？：；～'.decode('utf8')
        for text in texts:
            if text in punt_list:  # 检查标点符号下一个字符是否还是标点
                sentences.append(texts[start:i + 1])  # 当前标点符号位置
                start = i + 1  # start标记到下一句的开头
                i += 1
            else:
                i += 1  # 若不是标点符号，则字符位置继续前移
        if start < len(texts):
            sentences.append(texts[start:])  # 这是为了处理文本末尾没有标点符号的情况
        return sentences
    sentencess = cleansent_tokenizer(sentenceString)
    shuu = []
    if sentencess:
        wwf = ['原标题', '报道', ')', '）', '(', '（', '#', '本报记者', '编辑', '来源', '作者', '点击', '观看', '欣赏', '记者','出品']
        for ww in wwf:
            if ww in sentencess[-1]:
                shuu.append(-1)
        if shuu:
            del sentencess[-1]
    sentencessString = ''
    for sentencee in sentencess:
        sentencessString = sentencessString + sentencee
    print(sentencessString)
    return sentencessString
# 一架日本航空自卫队f-35a隐形战机在日本青森县附近空域训练时与地面失联，日本共同社10日获悉，疑似失联战机的部分机身部件在青森县周边海域被发现。日本政府相关人士也证实，涉事战机坠毁的可能性极大。搜救工作仍在持续。f-35a消失地点在距离三泽基地东北方向约135公里的太平洋海面上，未能确认飞行员是否弹射逃生。目前海上自卫队的巡逻机及舰艇、海上安保厅的巡逻船正在现场海域附近进行搜索。原先日本计划推动f-35的国产化，但随后由于成本太高而放弃。2018年9月28日，美国海军陆战队一架f-35b战斗机在南卡罗来纳训练时坠毁。此前f-35也多次暴露出严重故障。2018年4月，五角大楼承认包括f-22、f-35在内的多型战机制氧设备存在问题，可能导致飞行员在飞行过程中因缺氧而昏迷。更早的2017年6月，日本本土组装的首架f-35a试飞时也曾出现故障，被迫在名古屋机场紧急降落。
# print(getAbstract('一架日本航空自卫队F-35A隐形战机在日本青森县附近空域训练时与地面失联，日本共同社10日获悉，疑似失联战机的部分机身部件在青森县周边海域被发现。日本政府相关人士也证实，涉事战机坠毁的可能性极大。搜救工作仍在持续。据日空自方面透露，战机失联后，空自巡逻机以及海自护卫舰、日本海上保安厅巡逻船等多方进行了彻夜搜救，但并未探测到任何求救信号。**3月底，日本防卫省刚宣布该国第一个F-35A隐形战机中队成立。不料4月9日日本航空自卫队发布公告称，一架F-35A战机在训练时“从雷达上消失”，疑似坠毁。日本防相岩屋毅随后宣布，自卫队剩余的12架F-35A立刻停飞。**日本共同社称，为实施战机对战机训练，当天晚上7时左右，共4架F-35A从航空自卫队三泽基地起飞。7时25分，其中一架F-35A从基地的雷达上消失，“有可能已坠落”。F-35A消失地点在距离三泽基地东北方向约135公里的太平洋海面上，未能确认飞行员是否弹射逃生。目前海上自卫队的巡逻机及舰艇、海上安保厅的巡逻船正在现场海域附近进行搜索。原先日本计划推动F-35的国产化，但随后由于成本太高而放弃。按计划，日本未来将采购共计147架F-35系列战斗机。F-35A号称是难以被雷达侦测到的隐形战机，为何航空自卫队依然能通过雷达监视其行踪呢?据专家介绍，隐形战机在日常训练飞行时为便于观测，通常会挂载能增大雷达反射面积的“龙伯透镜”，此举同时还可以让外界无法获得隐形战机的真实雷达信号特征，从而保持它的神秘面纱不被潜在对手探知。据介绍，F-35共分为空军型F-35A、海军陆战队型F-35B和海军舰载型F-35C。共同社称，美日人士表示，此次若确认坠机，将是F-35A的首例坠毁。2018年9月28日，美国海军陆战队一架F-35B战斗机在南卡罗来纳训练时坠毁。此前F-35也多次暴露出严重故障。2018年4月，五角大楼承认包括F-22、F-35在内的多型战机制氧设备存在问题，可能导致飞行员在飞行过程中因缺氧而昏迷。更早的2017年6月，日本本土组装的首架F-35A试飞时也曾出现故障，被迫在名古屋机场紧急降落。**路透社称，就在3月26日，日本刚宣布在三泽基地组建第一个F-35A中队。此前日本已拥有13架F-35A。原先日本计划推动F-35的国产化，但随后由于成本太高而放弃。按计划，日本未来将采购共计147架F-35系列战斗机。F-35A号称是难以被雷达侦测到的隐形战机，为何航空自卫队依然能通过雷达监视其行踪呢?据专家介绍，隐形战机在日常训练飞行时为便于观测，通常会挂载能增大雷达反射面积的“龙伯透镜”，此举同时还可以让外界无法获得隐形战机的真实雷达信号特征，从而保持它的神秘面纱不被潜在对手探知。据介绍，F-35共分为空军型F-35A、海军陆战队型F-35B和海军舰载型F-35C。共同社称，美日人士表示，此次若确认坠机，将是F-35A的首例坠毁。2018年9月28日，美国海军陆战队一架F-35B战斗机在南卡罗来纳训练时坠毁。此前F-35也多次暴露出严重故障。2018年4月，五角大楼承认包括F-22、F-35在内的多型战机制氧设备存在问题，可能导致飞行员在飞行过程中因缺氧而昏迷。更早的2017年6月，日本本土组装的首架F-35A试飞时也曾出现故障，被迫在名古屋机场紧急降落。**F-35A号称是难以被雷达侦测到的隐形战机，为何航空自卫队依然能通过雷达监视其行踪呢?据专家介绍，隐形战机在日常训练飞行时为便于观测，通常会挂载能增大雷达反射面积的“龙伯透镜”，此举同时还可以让外界无法获得隐形战机的真实雷达信号特征，从而保持它的神秘面纱不被潜在对手探知。据介绍，F-35共分为空军型F-35A、海军陆战队型F-35B和海军舰载型F-35C。共同社称，美日人士表示，此次若确认坠机，将是F-35A的首例坠毁。2018年9月28日，美国海军陆战队一架F-35B战斗机在南卡罗来纳训练时坠毁。此前F-35也多次暴露出严重故障。2018年4月，五角大楼承认包括F-22、F-35在内的多型战机制氧设备存在问题，可能导致飞行员在飞行过程中因缺氧而昏迷。更早的2017年6月，日本本土组装的首架F-35A试飞时也曾出现故障，被迫在名古屋机场紧急降落。**据介绍，F-35共分为空军型F-35A、海军陆战队型F-35B和海军舰载型F-35C。共同社称，美日人士表示，此次若确认坠机，将是F-35A的首例坠毁。2018年9月28日，美国海军陆战队一架F-35B战斗机在南卡罗来纳训练时坠毁。此前F-35也多次暴露出严重故障。2018年4月，五角大楼承认包括F-22、F-35在内的多型战机制氧设备存在问题，可能导致飞行员在飞行过程中因缺氧而昏迷。更早的2017年6月，日本本土组装的首架F-35A试飞时也曾出现故障，被迫在名古屋机场紧急降落。'))
# db = pymysql.connect(host='47.100.163.195', user='recommend', password='recommend', database='test', port=3306)
# # 使用cursor()方法创建一个游标对象cursor
# cursor = db.cursor()
# # 查询
# sqlb = "SELECT newsid,content FROM News where abstract is null and website = 'cnr';"
# try:
#     # 执行sql语句
#     cursor.execute(sqlb)
#         # 通过fetchall获取results对象并打印结果
#     results = cursor.fetchall()
#     print('success')
#     # base_dir = os.getcwd()
#     # fiename = base_dir + '/AbsProblem.txt'
#     # for wert in results:
#     #     with open(fiename, 'a', encoding='utf-8') as f:
#     #         newid = wert[0]
#     #         content = wert[1]
#     #         abstract = getAbstract(wert[1])
#     #         f.write(newid + '\n')
#     #         f.write(content + '\n')
#     #         f.write(abstract + '\n')
# except:
#     print('failed')
# db.close()

# dba = pymysql.connect(host='47.100.163.195', user='recommend', password='recommend', database='test', port=3306)
# # 使用cursor()方法创建一个游标对象cursor
# cursora = dba.cursor()
# for wert in results:
#     # tup = ()
#     newsid = wert[0]
#     abstract = getAbstract(wert[1])
#     # tup = (abstract, newsid)
#     # tup1 = tup1 + tup
#     sqla = "UPDATE News SET abstract = %s where newsid = %s;"
#     try:
#         cursora.execute(sqla, (abstract, newsid))
#         dba.commit()
#         print('success')
#     except:
#         dba.rollback()
#         print('failed')
# dba.close()