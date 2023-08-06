# -*-coding=utf-8-*-
import click
import json
import logging
from zlado.aliyun import ali_cli
from zlado import ado_ini
import os


def get_ecses():
    cfg = ado_ini.read_cfg()
    print('regions:',cfg.get('config', 'regionids').split(','))
    cli = ali_cli.AliCli(cfg.get('config', 'accesskeyid'),
                         cfg.get('config', 'accesskeysecret'),
                         cfg.get('config', 'regionids').split(','))
    ecses= [ecs for ecs in cli.ecses_iterator()]
    # ecses = sorted(ecses, key=lambda x: x.hostname, reverse=False)
    ecses = sorted(ecses, key=lambda x: x.createTime, reverse=False)
    return ecses
import signal
# 恢复为默认状态

@click.command()
def cli():
    ecses = get_ecses()
    while True:
        try:
            os.system('clear')
            for i in range(len(ecses)):
                print(''.join([str(i + 1), ':', ecses[i].__str__()]))

            indexstr = input('请选择ECS序号:')
            if not indexstr.isdigit():
                continue
            if int(indexstr) > len(ecses):
                continue

            cur_ecs = ecses[int(indexstr) - 1]
            sship = cur_ecs.ip
            # sship = '127.0.0.1'
            print('ecs', ':', cur_ecs.__str__())
            # 防止卡死 《python 执行 shell 命令卡死》  @see https://zhuanlan.zhihu.com/p/266392974
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)
            os.system('ssh ' + sship)
        except SyntaxError as e:
            pass
        except SyntaxError as e:
            try:
                logging.error(e.msg, e)
            except:
                pass
            pass



if __name__ == '__main__':
    cli()
