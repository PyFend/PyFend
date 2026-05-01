import click

from pyfend.cli.hash_probe import hash_probe_cmd


@click.group()
@click.version_option(package_name="pyfend")
def main() -> None:
    """PyFend — Collection of cybersecurity tools for CLI and library use."""


main.add_command(hash_probe_cmd)
