from gitrenametool.Utils import FileUtil, SubUtil, ShellUtil
import click
import click.types
from click import Context


def version():
    # wait poetry fix up: https://github.com/python-poetry/poetry/issues/1338
    # with open("pyproject.toml") as f:
    #     ret = re.findall(r'version = "(\d+\.\d+\.\d+)"', f.read())
    #     return ret[0]
    return "0.0.1"



# @click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.command()
@click.version_option(version(), "-V", "--version")
@click.option('--dir', default="./", help='dir name',required=True )
@click.option('--sname',  help='source name',required=True)
@click.option('--tname', help='target name',required=True)
def cli(dir:str,sname:str, tname:str):
    """rename git`s files dirs ."""
    Dirlist, Filelist = SubUtil.getAllSub(dir)
    source=sname
    target=tname
    for diritem in Dirlist:
        print(diritem)
        tardirPath=FileUtil.replacefilepath(sourcepath=diritem,source=source,target=target)
        ispathexists=FileUtil.ispathexists(tardirPath)
        FileUtil.makedirs(tardirPath)
        
    for fileitem in Filelist:
        targetfilepath=FileUtil.replacefilepath(sourcepath=fileitem,source=source,target=target)
        sourcefile=fileitem#.replace(path,"")
        targetfile=targetfilepath#.replace(path,"")
        isgitexists=ShellUtil.isgitexists(sourcefile)
        if isgitexists:
            targetdir=FileUtil.getfiledir(targetfile)
            FileUtil.makedirs(targetdir)
            ShellUtil.gitmvfile(sourcefile,targetfile)


if __name__ == "__main__":
    cli()