import os
import argh
import re
from tqdm import tqdm
import mmap

def get_num_lines(filePath):
    fp = open(filePath,'r+')
    buf = mmap.mmap(fp.fileno(),0)
    lines=0
    while buf.readline():
        lines+=1
    return lines

def deleteFromList(dryRunFlag,listFile):
    "[dryRunFlag: y, n] [delete file: delete file must contained absolute path]"
    if re.search(r'(y|Y)',dryRunFlag) :
        dryRunFlag = True
    elif re.search(r'(n|N)',dryRunFlag) :
        dryRunFlag = False
    else :
        print ('Check dryRunFlag')
        return 1
    if os.path.isfile(listFile):        
        rsltLog = open(listFile+'_rslt','wb')
        deletedFileCount = 0
        totalFiles = 0
        with open(listFile) as delFiles:
            for delFile in tqdm(delFiles, total=get_num_lines(listFile)):
                totalFiles += 1
                stripedFileName = delFile.rstrip()
                if os.path.isfile(stripedFileName):
                    deletedFileCount += 1                  
                    if not dryRunFlag: # when dryrunflag True didn't remove
                        os.remove(stripedFileName)
                        rslt = stripedFileName+" was removed\n"
                        rsltLog.write(rslt.encode())
        delFiles.close()
        rsltLog.close()
    else:
        print("Check list file")
        return 0
    if dryRunFlag:
        print('Dry Run Result : Delete Files count is '+str(totalFiles)+' and If run delete those '+str(deletedFileCount)+" files will removed.")
    elif not dryRunFlag :
        print ('Delete Result : Total delete Files count is '+str(totalFiles)+' and '+str(deletedFileCount)+" files are removed.")

parser = argh.ArghParser()
parser.add_commands([deleteFromList])

if __name__ == "__main__":
    parser.dispatch()
