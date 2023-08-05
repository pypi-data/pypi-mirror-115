import click
import requests

from quake import Quake360, __token__

api = '/api/v3/search/quake_host'


@click.command()
@click.argument('ip')
def host(ip):
    """查看IP信息
    """
    qk360 = Quake360(__token__)
    jobj = qk360.host(query='ip:"{}"'.format(ip))
    if jobj is None:
        return

    if jobj['data'] == []:
        return

    click.secho('数据概览：', fg='green')
    location = jobj['data'][0]['location']


    print('自治域编号：', jobj['data'][0].get('asn', '--'))
    print('自治域名称：', jobj['data'][0].get('org', '--'))
    print('主机名：', jobj['data'][0].get('hostname', '--'))
    print('操作系统：', jobj['data'][0].get('os_name', '--'))
    print('操作系统版本：', jobj['data'][0].get('os_version', '--'))
    print('运营商：', location.get('isp', '--'))
    print('IP所有者：', location.get('owner', '--'))
    print()

    click.secho('地理位置：', fg='green')
    print('国家：', location.get('country_cn', '--'))
    print('省份：', location.get('province_cn', '--'))
    print('城市：', location.get('city_cn', '--'))
    print('gps：', location.get('gps', '--'))
    print()
    

    
    click.secho('域名：', fg='green')
    domains = []
    for item in jobj.get('data')[0].get('domains'):
        domains.append(item['domain'])
    for item in sorted(domains):
        print(item)
    print()

    click.secho('端口列表：', fg='green')
    for item in jobj.get('data')[0].get('services'):
        print('  端口：', item['port'])
        print('  传输层：', item['transport'])
        print('  服务协议：', item['name'])
        print('  产品：', item['product'])
        print('  版本：', item['version'])
        print()