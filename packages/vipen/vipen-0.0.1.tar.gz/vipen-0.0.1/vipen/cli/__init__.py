from . import server
from .main import cli


def main():
    from . import cluster, domain, fix, key, monitoring, provider, server

    cli(auto_envvar_prefix="VIPIEN")
