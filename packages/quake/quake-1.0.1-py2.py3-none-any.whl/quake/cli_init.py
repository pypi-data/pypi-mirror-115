import click
import toml

from quake import __cfg_path__


@click.command()
@click.argument('api_key')
def init(api_key):
    """初始化Quake，请用个人信息中的API Key
    """
    with open(__cfg_path__, 'w') as f:
        toml.dump({'api_key':api_key}, f)
