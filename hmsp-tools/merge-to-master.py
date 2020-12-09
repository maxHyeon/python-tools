# to-do
# get root dir, option
# option 1 -> [-m] [merge from branch name] [merge to branch name]  merge to branch name 
# search all child dir below root dir
# 0. if the dir has git repo, ask user to processing merge
# 1. checkout to merge from branch
# 2. checkout to merge to branch 
# 3. git merge [merge from branch]
import os
import sys
import sh
from sh import git

MyErrors = {"noDirExist":"Please Check Dir Path" }
# git config --get remote.origin.url
def searchDir(rootDirPath):
    if os.path.isdir(rootDirPath)  == False:
        print (MyErrors.get("noDirExist"))
    elif os.path.isdir(rootDirPath)  == True:
        print (os.listdir(rootDirPath))
        print (os.listdir(rootDirPath+"/elk-service"))

def main():
    searchDir(sys.argv[1])
    print(git.branch("-v"))



if __name__ == "__main__":
    main()