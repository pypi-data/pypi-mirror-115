import os
#** 替换文件路径 *
def replacefilepath(sourcepath:str,source:str,target:str):
    return sourcepath.replace(source, target)

def ispathexists(path:str):
    # if os.path.isdir(path):
    #     print ("it's a directory")
    # elif os.path.isfile(path):
    #     print ("it's a normal file")
    # else:
    #     print ("it's a special file(socket,FIFO,device file)")
    return os.path.exists(path=path)

def makedirs(path:str):
    os.makedirs(path,exist_ok=True)

def getfiledir(path:str):
    dir_path = os.path.dirname(os.path.realpath(path))
    return dir_path