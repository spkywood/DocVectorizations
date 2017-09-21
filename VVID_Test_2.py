# -*-encoding:utf-8 -*-
import codecs
import re
pat = r'vvid=[A-Z0-9-]{36}'

#read logfile by lines
logFile = codecs.open('app.log', 'r', 'utf-8', 'ignore')
logFile_convert = logFile.readlines()[::-1]     #convert

resultLog = codecs.open('app_convert.log', 'w+', 'utf-8', 'ignore')
resultLog.writelines(logFile_convert)

row_line = len(logFile_convert)
print "All logfile lines:", row_line, '\n'

VVID_List = []      #All VVID list
vvid_line = []      #include VVID line
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
    print VVID_List[j]

cutLine_num = []
for cut_item in range(1,VVID_List_length):
    if VVID_List[cut_item] != VVID_List[cut_item - 1]:
        cutLine_num.append(vvid_line[cut_item - 1])
        print cutLine_num
        #print vvid_line[cut_item - 1]