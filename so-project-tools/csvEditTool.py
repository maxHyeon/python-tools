# TODO 
# 1. input Path, option (-d *delete),keyword(input python list type a,b,c) ,[file type ex) .mef3 ]
# 2. open the file in folder
# 3. delete line 
# 4. save
# 5. print list 

import os
import sys
import csv

def stringWithCommaToList(inputStr):
    return inputStr.split(',')

def printUseage():
    print('useage : csvEditTool.py (targetDir) (option) [follows ]')
    print('---- Options ----')
    print('-d : delete keywordList line ((keywordList - input python list type a,b,c) (fileType ex) .mef3))')

def isLineContainKeyword (targetLine,keywordList):
    for keyword in keywordList:
        if keyword in targetLine:
            return True
    return False

def csvLineDel(targetFile,keywordList):
    f=open(targetFile,'r')
    rdr=csv.reader(f)
    lines=[]
    for line in rdr:
        if isLineContainKeyword (line[0] ,keywordList) == False :
            lines.append(line)
        else:
            print('fix')
            
    f.close()
    f=open(targetFile,'wb')
    wr=csv.writer(f)
    wr.writerows(lines)
    f.close()

def delMefDelUser(targetDir,keywords,fileType):
    if os.path.isdir(targetDir)==False:
        print(targetDir+' dir isn\'t exist')
        return
    keywordList=stringWithCommaToList(keywords)
    targetFileList=os.listdir(targetDir) 
    for targetFile in targetFileList:
        if fileType in targetFile:
            csvLineDel(targetDir+'\\'+targetFile,keywordList)

def main():
    if len(sys.argv) <= 2 :
        printUseage()
    else :
        if sys.argv[2] == '-d':
            delMefDelUser(sys.argv[1],sys.argv[3],sys.argv[4])
        else :
            printUseage()  


if __name__ == "__main__":
    main()