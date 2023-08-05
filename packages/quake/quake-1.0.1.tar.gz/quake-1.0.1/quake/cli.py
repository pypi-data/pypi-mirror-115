import sys

import click

from quake import __version__, cli_host, cli_info, cli_init, cli_domain


@click.group()
@click.version_option(version=__version__)
def main(args=None):
    """CLI for https://quake.360.cn/"""
    return 0


main.add_command(cli_init.init)
main.add_command(cli_info.info)
main.add_command(cli_host.host)
main.add_command(cli_domain.domain)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
