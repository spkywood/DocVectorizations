# -*-encoding:utf-8 -*-
import codecs
import re
pat = r'vvid=[A-Z0-9-]{36}'

#read logfile by lines
logFile = codecs.open('ppbox.log', 'r', 'utf-8', 'ignore')
logFile_convert = logFile.readlines()[::-1]     #convert

resultLog = codecs.open('ppbox_convert.log', 'w+', 'utf-8', 'ignore')
resultLog.writelines(logFile_convert)

row_line = len(logFile_convert)
print "All logfile lines:", row_line, '\n'

#include vvid lines
vvid_lines =  []
for i in range(0, row_line):
    if "vvid=" in logFile_convert[i]:
        vvid_lines.append(i)
#print vvid_lines
#get the vvid in lines
start = 0
vvid_lines_nums =len(vvid_lines)
VVID_List = []
VVID_Dic = {}
for i in range(0, vvid_lines_nums):
    re.match(pat, logFile_convert[vvid_lines[i]])
    print vvid_lines[i]
    #print re.search(pat, logFile_convert[vvid_lines[i]]).group()
    matches = re.search(pat, logFile_convert[vvid_lines[i]])
    if matches:
        VVID_List.append(matches.group())
        """for j in range(1, vvid_lines_nums):
            if VVID_List[j] != VVID_List[j-1]:
                print vvid_lines[j-1]
            else:
                pass"""
        print VVID_List[i]
    else:
        VVID_List.append(VVID_List[i-1])
        print VVID_List[i-1]    

VVID_Dic = dict(zip(vvid_lines, VVID_List))
print VVID_Dic
print len(VVID_Dic)