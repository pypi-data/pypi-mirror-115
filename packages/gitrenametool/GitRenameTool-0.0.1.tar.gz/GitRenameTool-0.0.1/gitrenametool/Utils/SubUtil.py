import os
# 方式二，通过递归调用一层层获取
def getAllSub(path, dirlist=[], filelist=[]):
    flist = os.listdir(path)
    for filename in flist:
        subpath = os.path.join(path, filename)
        if os.path.isdir(subpath):
            dirlist.append(subpath)		# 如果是文件夹，添加到文件夹列表中
            getAllSub(subpath, dirlist, filelist)	# 向子文件内递归
        if os.path.isfile(subpath):
            filelist.append(subpath)	# 如果是文件，添加到文件列表中
    return dirlist, filelist
