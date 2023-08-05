import pandas as pd
import click
import requests

from quake import Quake360, __token__

api = '/api/v3/search/quake_host'


@click.command()
@click.argument('name')
def domain(name):
    """查看域名信息
    """
    qk360 = Quake360(__token__)
    jobj = qk360.service(query='domain:"{}"'.format(name))
    if jobj is None:
        return

    if jobj['data'] == []:
        return

    df = pd.DataFrame(columns=('IP', '传输协议', '端口', 'ASN',
                               '服务协议', '网站服务器', '运营商', '组织'))

    print(jobj['meta']['pagination']['total'])
    result = {}
    for item in jobj['data']:
        ip = item['ip']
        transport = item['transport']
        port = item['port']

        asn = item['asn']
        org = item['org']
        isp = item['location']['isp']

        http = 'http' in item['service']
        server = None
        if http:
            server = item['service']['http']['server']
        tls = 'tls' in item['service']
        protocol = ''
        if http and tls:
            protocol = 'http/ssl'
        elif http:
            protocol = 'http'
        elif tls:
            protocol = 'ssl'

        df.loc[len(df)] = [ip, transport, port, asn, protocol, server, isp, org]

    df = df.drop_duplicates()

    from tabulate import tabulate
    print(tabulate(df, headers='keys'))
