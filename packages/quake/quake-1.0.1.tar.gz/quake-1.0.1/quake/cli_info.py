import click

from quake import Quake360, __token__


@click.command()
def info():
    """用户信息，每次查询都会消耗积分。
    """
    qk360 = Quake360(__token__)
    jobj = qk360.info()
    if jobj is None:
        return
    click.secho('月度积分：', nl=False, fg='green')
    print(jobj.get('data').get('credit'))
    click.secho('长效积分：', nl=False, fg='green')
    print(jobj.get('data').get('persistent_credit'))
    click.secho('用户类型：', nl=False, fg='green')
    for item in jobj.get('data').get('role'):
        print(item['fullname'], end=' ')
    print()
