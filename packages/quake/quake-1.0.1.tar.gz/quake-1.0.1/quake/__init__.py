import os

import requests
import toml

__author__ = """King Orz"""
__email__ = 'kin9-0rz@outlook.com'
__version__ = '1.0.1'


__home__ = os.path.expanduser('~')
__cfg_path__ = os.path.join(__home__, '.quake.toml')

__token__ = ""
try:
    __token__ = toml.load(__cfg_path__).get('api_key', None)
except FileNotFoundError:
    pass

__headers__ = {
    "X-QuakeToken": __token__
}


class Quake360:
    def __init__(self, token) -> None:
        self.token = token
        self.headers = {
            "X-QuakeToken": self.token
        }

    def info(self):
        """用户信息

        :return: 返回请求结果
        :rtype: json
        """
        api = 'api/v3/user/info'
        response = requests.get(
            url="https://quake.360.cn/{}".format(api), headers=__headers__)

        if response.status_code == 401:
            print('API Key Error')
            return

        return response.json()

    def host(self, query:str='*', start:int=0, size:int=10, ignore_cache:bool=False, start_time:str=None, end_time:str=None):
        """主机数据查询接口

        :param start_time: 查询起始时间，接受2020-10-14 00:00:00格式的数据，时区为UTC;仅付费用户能够指定查询时间，非付费用户默认仅查询近一年的数据
        :type start_time: str
        :param end_time: 查询截止时间，接受2020-10-14 00:00:00格式的数据，时区为UTC;仅付费用户能够指定查询时间，非付费用户默认仅查询近一年的数据
        :type end_time: str
        :param query: 查询语句, defaults to '*'
        :type query: str, optional
        :param start: 分页起始, defaults to 0
        :type start: int, optional
        :param size: 分页大小, defaults to 10
        :type size: int, optional
        :param ignore_cache: 是否忽略缓存, defaults to False
        :type ignore_cache: bool, optional
        :return: 查询结果
        :rtype: json
        """
        api = '/api/v3/search/quake_host'
        data = {
            "query": query,
            "start": start,
            "size": size,
            "ignore_cache": ignore_cache,
        }

        if start_time is not None:
            data = {
                "query": query,
                "start": start,
                "size": size,
                "ignore_cache": ignore_cache,
                "start_time": start_time,
                "end_time": end_time,
            }

        response = requests.post(
            url="https://quake.360.cn/{}".format(api), headers=__headers__, json=data)

        if response.status_code == 401:
            print('API Key Error')
            return
        if response.status_code == 500:
            print(response.text)
            return
        return response.json()

    def service(self, query:str='*', start:int=0, size:int=10, ignore_cache:bool=False, start_time:str=None, end_time:str=None):
        """主机数据查询接口

        :param start_time: 查询起始时间，接受2020-10-14 00:00:00格式的数据，时区为UTC;仅付费用户能够指定查询时间，非付费用户默认仅查询近一年的数据
        :type start_time: str
        :param end_time: 查询截止时间，接受2020-10-14 00:00:00格式的数据，时区为UTC;仅付费用户能够指定查询时间，非付费用户默认仅查询近一年的数据
        :type end_time: str
        :param query: 查询语句, defaults to '*'
        :type query: str, optional
        :param start: 分页起始, defaults to 0
        :type start: int, optional
        :param size: 分页大小, defaults to 10
        :type size: int, optional
        :param ignore_cache: 是否忽略缓存, defaults to False
        :type ignore_cache: bool, optional
        :return: 查询结果
        :rtype: json
        """
        api = '/api/v3/search/quake_service'
        data = {
            "query": query,
            "start": start,
            "size": size,
            "ignore_cache": ignore_cache,
        }

        if start_time is not None:
            data = {
                "query": query,
                "start": start,
                "size": size,
                "ignore_cache": ignore_cache,
                "start_time": start_time,
                "end_time": end_time,
            }

        response = requests.post(
            url="https://quake.360.cn/{}".format(api), headers=__headers__, json=data)

        if response.status_code == 401:
            print('API Key Error')
            return
        if response.status_code == 500:
            print(response.text)
            return
        return response.json()
