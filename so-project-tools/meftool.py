import os
import sys
import csv
import re
import argh


def printUseage():
    print ('useage: meftool.py (folder pwd) (option) [output_filename]')
    print ('--- Options ---')
    print ('-b : bigfix gather file name prefix delete ex:file_0_')
    print ('-m [output filename fullpwd]: file list make csv with outputfilename')

def delPrefix(targetDir):
    "bigfix gather file name prefix delete ex:file_0_'"
    if os.path.isdir(targetDir)==False:
        print(targetDir+' dir isn\'t exist')
    else:
        changedFile = 0
        destFiles = os.listdir(targetDir)
        for i in destFiles:
            oldFileName = i
            if oldFileName[:7] == 'file_0_':
                changedFile += 1; 
                os.rename(targetDir+'\\'+oldFileName ,targetDir+'\\'+oldFileName[7:])
        
        print(str(changedFile)+' was changed')
        resultFiles = os.listdir(targetDir)
   
def makeMefHostList(targetDir,outputFile):
    "[output filename fullpwd]: file list make csv with outputfilename"
    workDir = os.getcwd()
    f = open(workDir+'\\'+outputFile,'wb+')    
    regex = re.compile (r'^[a-zA-Z]*_[0-9]*_') # KBLI_[DATE]_ find
 
    destFiles = os.listdir(targetDir)

    for i in destFiles :
        if i[-5:] == '.mef3' :
            mefPrefix = regex.search(i)
            if mefPrefix != None :
                trimResult = i[:-5].replace(str(mefPrefix.group()),"",1)
                f.write(trimResult+'\n')

    f.close()


parser = argh.ArghParser()
parser.add_commands([delPrefix,makeMefHostList])

def main():
    if len(sys.argv) <= 2 :
       printUseage()
    else :
        if sys.argv[2] == '-b':
            delPrefix(sys.argv[1])
        if sys.argv[2] == '-m' and len(sys.argv) >= 4 :
            makeMefHostList(sys.argv[1],sys.argv[3])
        else :
            printUseage()

if __name__ == "__main__":
    parser.dispatch()