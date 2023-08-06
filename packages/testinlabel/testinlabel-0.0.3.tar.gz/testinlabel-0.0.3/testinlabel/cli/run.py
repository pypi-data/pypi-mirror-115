import click
import json
import os
import requests
import shutil
import sys
from testinlabel.cli import account

import testinlabel
from testinlabel.TLA import TLA


def _download(url, savePath):
    res = requests.get(url)
    saveDir = os.path.split(savePath)[0]
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    with open(savePath, 'wb') as f:
        f.write(res.content)

def printVersion(ctx):
    if hasattr(testinlabel, "VERSION"):
        click.echo("")
        click.echo(".___________. __           ___     ")
        click.echo("|           ||  |         /   \     ")
        click.echo("`---|  |----`|  |        /  ^  \    ")
        click.echo("    |  |     |  |       /  /_\  \   ")
        click.echo("    |  |     |  `----. /  _____  \  ")
        click.echo("    |__|     |_______|/__/     \__\\")
        click.echo("")
        click.echo(f'    TDA Version {testinlabel.VERSION}')
        click.echo('    more about: http://ai.testin.cn/')
        click.echo('    login: https://label.testin.cn/')
        click.echo("")
        ctx.exit()
    click.echo('TLA Version 0.0.1')
    ctx.exit()


@click.group()
@click.option("-ak", "--accessKey", 'access_key', default="", help="access key to Testin annotation system, see: http://label.testin.cn/v/secret-key")
@click.option("-sk", "--secretKey", 'secret_key', default="")
@click.option("-h", "--host", 'host', default="https://label.testin.cn/", help="domain name that access to annotation system you would like to operate, default will be: https://label.testin.cn/")
@click.option('--debug/--no-debug', default=True, help="using debug mod or not, default is False")
@click.pass_context
def main(ctx, access_key, secret_key, host, debug):
    """
    testin annotation system data export tool
    """
    info = {
        "access_key": access_key,
        "secret_key": secret_key,
        "host": host,
        "DEBUG": debug
    }

    _tla = None

    if access_key == "":
        configFile = account._config_filepath()
        if os.path.exists(configFile):
            with open(configFile, "r", encoding="utf-8") as cf:
                if cf.read() != "":
                    info = account._getConf()
                    info["DEBUG"] = debug

    if info["access_key"] != "":
        _tla = TLA(info["access_key"], info["secret_key"], info["host"])
        if info["DEBUG"]:
            _tla = TLA(info["access_key"], info["secret_key"], info["host"], debug=True)

    ctx.obj = _tla

@main.command()
@click.option("-k", "--task_key", 'taskKey', default="", help="the task you wolud like to oprate")
@click.pass_context
def template(ctx, taskKey):
    """ generate export code template """
    if ctx.obj == None:
        account._noLoginMessage()
    codeContent="""from testinlabel.exportAbstract import ExportAbstract # warning: don't edit this line !!!
from testinlabel.TLA import TLA     # warning: don't edit this line !!!

#import your packages

class Export(ExportAbstract):

    def __init__(self, tla: TLA):       # warning: don't edit this line !!!
        self.tla = tla                  # warning: don't edit this line !!!
        self.tla.SetKey("210723e32ad")  # warning: don't edit this line !!!
        self.tla.GetLabelData()         # warning: don't edit this line !!!

    def exec(self):
        # edit following code to
        for item in self.tla.taskList:
            print(item["imgUrl"])
"""
    with open("export.py", "w", encoding="utf-8") as sf:
        sf.write(codeContent)

    click.echo("script template generate success! script name: export.py")
    click.echo("use command: tla export export.py to export your data")
    click.echo("more: tla export --help")


@main.command()
@click.option("-f", "--script-file", 'file', default="", help="script file path")
@click.pass_context
def export(ctx, file):
    """ exec export """
    if ctx.obj == None:
        account._noLoginMessage()
    try:
        sys.path.append(os.path.split(file)[0])
        from export import Export
        ex = Export(ctx.obj)
        ex.exec()
    except Exception as e:
        print(e)
        raise Exception(f"can't import Export")

    click.echo("done!")

@main.command()
@click.pass_context
def version(ctx):
    """ show version """
    printVersion(ctx)
    ctx.exit()


@main.command()
@click.option("-ak", "--accessKey", 'access_key', default="", help="access key to Testin annotation system, see: http://label.testin.cn/v/secret-key")
@click.option("-sk", "--secretKey", 'secret_key', default="")
@click.option("-h", "--host", 'host', default="https://label.testin.cn/", help="domain name that access to annotation system you would like to operate, default will be: https://label.testin.cn/")
def config(access_key, secret_key, host):
    """ setting your account """
    configFile = account._config_filepath()
    if access_key == "":
        if account._check():
            click.echo("account:")
            print(account._getConf())
            exit()
    else:
        conf = {
            "access_key": access_key,
            "secret_key": secret_key,
            "host": host,
        }
        with open(configFile, "w") as config:
            json.dump(conf, config)
            click.echo("config success")
            print(conf)
            exit()

# @main.command()
# @click.option("-ds", "--datasetId", 'ds_id', default="", help="the dataset you wolud like to download")
# @click.option("-save", "--saveDir", 'save_dir', default="", help="save path for downloaded files")
# @click.pass_context
# def download(ctx, ds_id, save_dir):
#     """ download dataset data """
#     if ctx.obj == None:
#         account._noLoginMessage()
#
#     ctx.obj.SetDataset(ds_id)
#     saveDir = os.path.join(save_dir, ds_id)
#     if not os.path.exists(saveDir):
#         os.makedirs(saveDir)
#
#     page = 0
#     limit = 100
#     fileTotal = 1
#     while True:
#         offset = page * limit
#         fileData = ctx.obj.GetData(offset, limit)
#         if len(fileData["files"]) <= 0:
#             break
#         page += 1
#         for file in fileData["files"]:
#             picPath = file.path.split(ds_id)[1].strip("/")
#             basename = os.path.basename(picPath)
#             tmpPath = picPath.replace(basename, "").strip("/")
#
#             fileDir = os.path.join(saveDir, tmpPath)
#             if not os.path.exists(fileDir):
#                 os.makedirs(fileDir)
#
#             filePath = os.path.join(fileDir, tmpPath, basename)
#             if os.path.exists(filePath):
#                 fmd5 = util.getFileMd5(filePath)
#                 if fmd5 != file.md5:
#                     _download(file.url, filePath)
#                     if ctx.obj.debug:
#                         print(f"[SAVE_FILE]file total: {fileTotal}, truncate file, redo: [{filePath}]")
#                 else:
#                     if ctx.obj.debug:
#                         print(f"[SAVE_FILE]file total: {fileTotal}, file already exist: [{filePath}]")
#             else:
#                 _download(file.url, filePath)
#                 if ctx.obj.debug:
#                     print(f"[SAVE_FILE]file total: {fileTotal}, file download and save: [{filePath}]")
#
#             labelData = ctx.obj.GetFileAndLabel(fid=file.fid)
#             jsonname = ".".join(basename.split(".")[:-1])
#             jsonPath = os.path.join(fileDir, tmpPath, jsonname + "_label.json")
#             with open(jsonPath, "w", encoding="utf-8") as jf:
#                 json.dump(labelData.anotations.labels, jf)
#                 if ctx.obj.debug:
#                     print(f"[SAVE_LABEL]file total: {fileTotal}, save label data: [{jsonPath}]")
#
#             fileTotal += 1
#
#     if ctx.obj.debug:
#         print("done!")

@main.command()
@click.pass_context
def clearcache(ctx):
    """ clean up the SDK caches """
    dir = os.path.split(account._config_filepath())[0]
    shutil.rmtree(dir)
    click.echo("all caches are cleaned up! :)")
    exit()


if __name__ == '__main__':
    main(obj={})



