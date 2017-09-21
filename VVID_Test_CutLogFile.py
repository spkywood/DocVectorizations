# -*-encoding:utf-8 -*-
import codecs
import re
pat = r'vvid=[A-Z0-9-]{36}'

#logFile按行读入存储在list
logFile = codecs.open('app.log', 'r', 'utf-8', 'ignore')
logFile_convert = logFile.readlines()[::-1]     #convert

resultLog = codecs.open('app_convert.log', 'w+', 'utf-8', 'ignore')
resultLog.writelines(logFile_convert)

row_line = len(logFile_convert)
print "All logfile lines:", row_line, '\n'

VVID_List = []      #所有的VVID存储在list
vvid_line = []      #包含VVID的行
for i in range(0, row_line):
    re.match(pat, logFile_convert[i])
    matches = re.search(pat, logFile_convert[i])
    if matches:
        VVID_List.append(matches.group())
        vvid_item = i
        vvid_line.append(vvid_item)

VVID_List_length = len(vvid_line)   #The number of VVID
print "The number of the All vvid", VVID_List_length, '\n'     #include VVID line
for j in range(0, VVID_List_length):
    print vvid_line[j]
    print VVID_List[j], '\n'

cutLine_num = []
for cut_item in range(1,VVID_List_length):
    if VVID_List[cut_item] != VVID_List[cut_item - 1]:
        cutLine_num.append(vvid_line[cut_item - 1] + 1)

#找到需要分割的行        
print "Cut line_num"
print cutLine_num, '\n' 
#print vvid_line[cut_item - 1]

#从convert文件中按行读入，碰到在cutLine_num中的行输出
Cutfile_nums = len(cutLine_num)
print u"一共切割成",Cutfile_nums + 1, u"文件" 
flag = 0
for item in range(0, Cutfile_nums):
	#print item, flag, Cutfile_nums[item]
	#分割后文件名
	codecs.open('app_%d.log' % (item), 'w+', 'utf-8', 'ignore').writelines(logFile_convert[flag:cutLine_num[item]][::-1])
	if cutLine_num[item] == cutLine_num[-1]:
		#print item+1, cutLine_num[item], len(logFile_convert)
		codecs.open('app_%d.log' % (item+1), 'w+', 'utf-8', 'ignore').writelines(logFile_convert[cutLine_num[item]:][::-1])
	flag = cutLine_num[item]