import click
from InquirerPy import prompt
from vipen.core.logging import console
from vipen.core.task import TaskPool

from .main import cli
from .util import current_cluster, get_config, new_progress


@cli.command()
@click.pass_context
def fix(ctx):
    config = get_config(ctx)
    cluster = current_cluster(ctx)

    # Find stale servers (servers that exist in provider but not in our)
    stale_servers = []
    for provider in config.server_providers:
        for server in provider.fetch_cluster_servers(cluster):
            if server not in cluster.servers:
                stale_servers.append(server)
    if len(stale_servers) > 0:
        console.log(f"Found {len(stale_servers)} stale servers:")
        for s in stale_servers:
            console.log(f"{s.provider.name}/{s.name}")

        answer = prompt(
            {
                "message": "Should I destroy the servers?",
                "type": "confirm",
                "default": True,
            },
        )
        if answer[0]:
            with new_progress() as p:
                with TaskPool(progress=p) as pool:
                    for s in stale_servers:
                        pool.submit(s.pname, s.destroy())

    # Find missing servers
    missing_servers = []
    for server in cluster.servers:
        if server.provider.fetch_server(server.id) is None:
            missing_servers.append(server)
    if len(missing_servers) > 0:
        console.log(f"Found {len(stale_servers)} missing servers:")
        for s in missing_servers:
            console.log(s.pname)

        answer = prompt(
            {
                "message": "Should I remove them?",
                "type": "confirm",
                "default": True,
            },
        )
        if answer[0]:
            for server in missing_servers:
                cluster.servers.remove(server)

    # Updating DNS Records
    def provision(domain):
        yield from domain.provision()
        yield from domain.update_dns_with_servers(cluster.servers)
        return True

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for domain in cluster.domains:
                pool.submit(
                    f"{domain.name}",
                    provision(domain),
                )
