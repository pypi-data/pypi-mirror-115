import os


def gitmvfile(sourcefile,targetfile):
    if(sourcefile==targetfile):
        return
    cmd=f"git mv {sourcefile} {targetfile}"

    output= run_command(cmd=cmd)
    print(output)


def isgitexists(sourcefile):
    cmd=f"git log {sourcefile}"

    output= run_command(cmd=cmd)
    return output.__len__() !=0


if __name__=="__main__":
    gitmvfile("README.rst1","README.rst")

if __name__=="__main__":
    gitmvfile("README.rst1","README.rst")

def run_command(cmd: str) -> str:
    """返回系统命令的执行结果"""
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()