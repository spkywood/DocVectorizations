#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
  
""" 
功能：PyNLPIR文本预处理 
过程：文本分词，过滤停用词，词频统计，特征选择，文本表示    
"""  
  
import pynlpir  
import codecs  
import math  
  
pynlpir.open()  
  
#文本分词  
typelist = [u"会员节目",u"play错误",u"url错误",u"需要购买",u"直播无信号",u"节目不存在",u"网络下载失败",u"文件不存在",u"内核问题"] 

#E:\Python\file_test
typetxt = codecs.open('E:\\Python\\file_test\\logtype.log', 'w', encoding='utf-8')  
wordseg_result = codecs.open('E:\\Python\\file_test\\wordseg_result.log', 'w',encoding='utf-8')  
  
allresult = []  
for j in range(1,2):  
    for i in range(1,11):  
        typetxt.write(typelist[j-1] + "\n")  
        s = ""  
        singletext_result = []  
        print  (u'正在对第 %s 个文件夹的第 %s 个日志文本进行分词处理.....'%(j,i))  
        f = codecs.open('E:\\Python\\file_test\\%d\\%d.log' % (j,i),'rb','utf-8', 'ignore')  
        for line in f:  
            s += line.strip()
  
        for item in pynlpir.segment(s):  
            singletext_result.append(item[0])  
        allresult.append(singletext_result)  
  
typetxt.close()  
print (u'文本类别析出完毕！结果已输出至logtype.log！')  
#直接打印出结果  
#for singletext_result in allresult:  
#    for item in singletext_result:  
#       print item  
  
#所有结果写入一个txt，一行一个文本  
for singletext_result in allresult:  
    for item in singletext_result:  
        wordseg_result.write(item+'\n')  
    wordseg_result.write('\n')  
wordseg_result.close()  
print (u'分词完毕！分词结果已输出至wordseg_result.log！'+'\n')  
  
  
#过滤停用词  
stopwords = []  
delstopwords_alltxt = []  
  
st = codecs.open('E:\\Python\\file_test\\stopwords.log', 'rb', 'utf-8', 'ignore')  
delstopwords_result = codecs.open('E:\\Python\\file_test\\delstopwords_result.log' , 'w+',encoding='utf-8')  
  
for line in st:  
    line = line.encode('utf-8').strip()  
    stopwords.append(line)  
  
print (u'正在过滤停用词......')  
  
for singletext_result in allresult:  
    delstopwords_singletxt = []  
    for word in singletext_result:  
        word = word.strip()  
        if word not in stopwords:  
            #if word >= u'\u4e00' and word <= u'\u9fa5':#判断是否是汉字  
            delstopwords_singletxt.append(word)  
    delstopwords_alltxt.append(delstopwords_singletxt)  
  
for delstopwords_singletxt in delstopwords_alltxt:  
    for everyword in delstopwords_singletxt:  
        delstopwords_result.write(everyword + '\n')  
    delstopwords_result.write('\n')  
delstopwords_result.close()  
print (u'停用词过滤完毕！已将结果输出至delstopwords_result.log！'+'\n')  
  
  
#统计绝对词频统计TF  
getTF_alltxt_dic = {}  
getTF_result =  codecs.open('E:\\Python\\file_test\\getTF_result.log' , 'w+',encoding='utf-8')  
  
print (u'正在统计TF......')  
  
for delstopwords_singletxt in delstopwords_alltxt:  
    getTF_singletxt_dic = {}  
    for everyword in delstopwords_singletxt:  
        everyword = everyword.strip()  
        if everyword in getTF_singletxt_dic:  
            getTF_singletxt_dic[everyword] += 1  
        else:  
            getTF_singletxt_dic[everyword] = 1  
  
    getTF_singletxt_dic = sorted(getTF_singletxt_dic.items(), key=lambda d: d[1], reverse=1)  
  
  
    for a, b in getTF_singletxt_dic:  
        if b > 0:  
            getTF_result.write(a + '\t' + str(b) + '\n')  
    getTF_result.write('\n')  
  
getTF_result.close()  
print (u'TF值统计完毕！已将结果输出至getTF_result.log！'+'\n')  
  
  
#特征选择  
#计算所有类别DF  
alltext = []  
allwords = []  
  
delstopwords_result =  codecs.open('E:\\Python\\file_test\\delstopwords_result.log' , 'rb',encoding='utf-8')  
  
wordlist = []  
for line in delstopwords_result:  
    alltext.append(line)  
    words = line.strip('\n').split('\t')  
    for word in words:  
        if word:  
            wordlist.append(word)  
  
print u"原始文本词汇总数：", len(wordlist)  
print u"文本个数：", len(alltext)  
print u"词汇种数：", len(set(wordlist))  
  
print ('\n'+u'正在计算所有类别DF......')  
word_df = []  
for word in set(wordlist):  
    count = 0  
    for words in alltext:  
        if word in words:  
            count += 1  
    word_df.append([word, str(count)])  # 存储形式[word，DF]  
  
# 输出  
word_df.sort(key=lambda x: int(x[1]),reverse=True)  # 词频从大到小排序  
b = codecs.open('E:\\Python\\file_test\\DF_allclass_result.log', "a", encoding="utf-8")  
b.truncate()  
for item in word_df:  
    for word in item:  
        b.write(word+ '\t')  
    b.write( '\n')  
b.close()  
  
b = codecs.open('E:\\Python\\file_test\\DF_allclass_result.log', "rb", encoding="utf-8")  
for line in b:  
    line = line.split('\t')  
    if len(line[0])>1:  
        c  = codecs.open('E:\\Python\\file_test\\DF_allclass_result1.log', "a", encoding="utf-8")  
        c.write(line[0]+'\t'+line[1])  
        c.write('\n')  
c.close()  
  
print (u'所有类别DF值统计完毕！已将结果输出至DF_allclass_result1.txt！'+'\n')  
  
#特征选择  
#计算单一类别DF  
  
print (u'正在计算单一类别DF......')  
  
word_df2 = []  
d  = codecs.open('E:\\Python\\file_test\\DF_allclass_result1.log', "rb", encoding="utf-8")  
  
for line in d:  
    line = line.split()  
    word = line[0]  
  
    count_1 = 0  
    count_2 = 0  
    count_3 = 0  
    count_4 = 0  
    count_5 = 0  
    count_6 = 0  
    count_7 = 0  
    count_8 = 0  
    count_9 = 0  
  
    for words in alltext[0:500]:  
        if word in words:  
            count_1 += 1  
  
    for words in alltext[500:1000]:  
        if word in words:  
            count_2 += 1  
  
    for words in alltext[1000:1500]:  
        if word in words:  
            count_3 += 1  
  
    for words in alltext[1500:2000]:  
        if word in words:  
            count_4 += 1  
  
    for words in alltext[2000:2500]:  
        if word in words:  
            count_5 += 1  
  
    for words in alltext[2500:3000]:  
        if word in words:  
            count_6 += 1  
  
    for words in alltext[3000:3500]:  
        if word in words:  
            count_7 += 1  
  
    for words in alltext[3500:4000]:  
        if line[0] in words:  
            count_8 += 1  
  
    for words in alltext[4000:4500]:  
        if word in words:  
            count_9 += 1  
  
    word_df2.append([word,str(count_1),str(count_2),str(count_3),str(count_4),str(count_5),str(count_6),str(count_7),str(count_8),str(count_9)])  # 存储形式[word，DF]  
  
d.close()  
  
# 输出  
e = codecs.open('E:\\Python\\file_test\\DF_singleclass_result.log', "a", encoding="utf-8")  
for item in word_df2:  
    for term in item:  
        e.write(term+'\t')  
    e.write( '\n')  
e.close()  
  
print (u'单一类别DF值统计完毕！已将结果输出至DF_singleclass_result.log！'+'\n')  
  
#计算特征项信息熵  
print (u'正在计算信息熵......')  
  
IG = []  
g  = codecs.open('E:\\Python\\file_test\\DF_allclass_result1.log', "rb", encoding="utf-8")  
for line in g:  
    line = line.split()  
    word = line[0]  
    word2 = float(line[1])  
    PC = float(500)/float(4500)  
    PC_1 = float(PC) * 9  
    Entropy = -(float(PC_1)*float(math.log(PC_1,2)))  
    PT = float(word2)/float(len(alltext))  
    PT_1 = float(1) - PT  
  
    h = codecs.open('E:\\Python\\file_test\\DF_singleclass_result.log', "rb", encoding="utf-8")  
    lines = h.readline()  
    line = lines[:-1]  
    line = line.split()  
    PCT_evenplus = ( float(line[1]) + float(line[2]) + float(line[3]) + float(line[4]) + float(line[5]) + float(line[6]) + float(line[7]) + float(line[8]) )/float(word2)  
    PCT_evenplus_ = float(1) - float(PCT_evenplus)  
    E1 = - (float(PCT_evenplus) * float(math.log(PCT_evenplus, 2)))  
    E2 = -(float(PCT_evenplus_) * float(math.log(float(PCT_evenplus),2)))  
    exEtropy =float(PT) * float(E1) + float(PT_1) * float(E2)  
  
    IG_value = float(Entropy) - float(exEtropy)  
    IG.append([word, str(IG_value)])  # 存储形式[word，IG_value]  
  
IG.sort(key=lambda x: float(x[1]), reverse=True)  # 词频从大到小排序  
i = codecs.open('E:\\Python\\file_test\\IG_value.log', "a", encoding="utf-8")  
i.truncate()  
for item in IG:  
    for word in item:  
        i.write(word + '\t')  
    i.write('\n')  
i.close()  
  
h.close()  
g.close()  
print (u'信息增益值统计完毕！已将结果输出至IG_value.log！'+'\n')  
  
print (u'正在选择特征词......')  
j = codecs.open('E:\\Python\\file_test\\IG_value.log', "rb", encoding="utf-8")  
for line in j:  
    line = line.split()  
    if float(line[1])> -float(10):  
        k = codecs.open('E:\\Python\\file_test\\FeatureWords.log', "a", encoding="utf-8")  
        k.write(line[0])  
        k.write('\n')  
k.close()  
j.close()  
print (u'特征词选择完毕！已将结果输出至FeatureWords.log！'+'\n')  
  
f1 = codecs.open('E:\\Python\\file_test\\DF_allclass_result1.log', "rb", encoding="utf-8")  
f2 = codecs.open('E:\\Python\\file_test\\FeatureWords.log', "rb", encoding="utf-8")  
FeatureWords_value = codecs.open('E:\\Python\\file_test\\FeatureWords_value.log', "a", encoding="utf-8")  
  
dic = {}  
for line in f1:  
    line =line.strip('\n').split('\t')  
    dic[line[0]]=line[1]  
f1.close()  
  
for word in f2:  
    if word in dic:  
        FeatureWords_value.write(dic[word]+'\t'+dic[word]+'\n')  
f2.close()  
FeatureWords_value.close()  
  
  
#文档向量化  
print (u'正在进行文本向量化处理......')  
  
f1 = codecs.open('E:\\Python\\file_test\\DF_allclass_result1.log', "rb", encoding="utf-8")  
f2 = codecs.open('E:\\Python\\file_test\\FeatureWords.log', "rb", encoding="utf-8")  
FeatureWords_value = codecs.open('E:\\Python\\file_test\\FeatureWords_value.log', "a", encoding="utf-8")  
  
allfw=[]  
for line in f1:  
    dic = {}  
    line =line.strip('\n').split('\t')  
    dic[line[0]]=line[1]  
    allfw.append(dic)  
f1.close()  
  
#for dic in allfw:  
#   for k,v in dic.iteritems():  
#       print k,v  
  
fw=[]  
for line in f2:  
    line=line.strip('\n').split('\t')  
    fw.append(line[0])  
f2.close()  
  
#for word in fw:  
#   print word  
  
for dic in allfw:  
    for word in fw:  
        if word in dic:  
            for k, v in dic.iteritems():  
                FeatureWords_value.write(k+'\t'+v+'\n')  
FeatureWords_value.close()  
  
  
feture_word = []  
feture_word_dic = {}  
feture_word_dic2 = {}  
  
FeatureWords_value = codecs.open('E:\\Python\\file_test\\FeatureWords_value.log', "rb", encoding="utf-8")  
for line in FeatureWords_value:  
    line = line.split()  
    IDF = math.log(4500/float(line[1]),10)  
    feture_word.append(line[0])  
    feture_word_dic[line[0]] = line[1]  
    feture_word_dic2[line[0]] = IDF  
FeatureWords_value.close()  
  
getTF_result = codecs.open('E:\\Python\\file_test\\getTF_result.log', "rb", encoding="utf-8")  
all=[]  
for line in getTF_result:  
    line = line.strip('\n').split('\t')  
    single=[]  
    for words in line:  
        single.append(words)  
    all.append(single)  
  
FeatureWords_value = codecs.open('E:\\Python\\file_test\\FeatureWords_value.log', "rb", encoding="utf-8")  
alltext_vector = []  
for single in all:  
    vector = []
    for word in feture_word:  
        if word in single:
            tmax = single[1]  
            inde=single.index(word)      
            t = single[inde+1]  
        else:  
            t = 0  
        tf_idf = (float(t)/float(tmax))*float(feture_word_dic2[word])  
        vector.append(tf_idf)  
    alltext_vector.append(vector)  
  
for vector in alltext_vector[0:500]:  
    vector.append('Economy')  
for vector in alltext_vector[500:1000]:  
    vector.append('IT')  
for vector in alltext_vector[1000:1500]:  
    vector.append( 'Health')  
for vector in alltext_vector[1500:2000]:  
    vector.append('PE')  
for vector in alltext_vector[2000:2500]:  
    vector.append('Travel')  
for vector in alltext_vector[2500:3000]:  
    vector.append( 'Education')  
for vector in alltext_vector[3000:3500]:  
    vector.append('Enployment')  
for vector in alltext_vector[3500:4000]:  
    vector.append('Culture')  
for vector in alltext_vector[4000:4500]:  
    vector.append('Military')  
  
#for vector in alltext_vector:  
#  print vector  
#    for value in vector:  
#       print value  
  
data = codecs.open('E:\\Python\\file_test\\data.arff', "w+", encoding="utf-8")  
data.truncate()  
  
data.write(u'@relation'+' '+u'sougoucorpus'+'\n\n')  
for everyword in feture_word:  
    data.write(u'@attribute'+ ' '+ everyword +' '+u'numeric\n')  
data.write(u'@attribute type {Economy,IT,Health,PE,Travel,Educaiton,Enployment,Culture,Military}\n\n@data\n')  
for vector in alltext_vector:  
    for value in vector[:-1]:  
        data = codecs.open('E:\\Python\\file_test\\data.arff', "w+", encoding="utf-8")  
        data.write(str(value) + ',')  
    data.write(str(vector[-1]) + '\n')  
    data.close()  
  
print (u'文本向量化处理完毕！已将结果输出至data.arff！'+'\n')  
  
print (u'文本预处理结束！'+'\n')  