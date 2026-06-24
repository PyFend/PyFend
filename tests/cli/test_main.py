from click.testing import CliRunner

from pyfend.cli.__main__ import main


def test_main_help_lists_hash_probe_command() -> None:
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "hash-probe" in result.output


def test_hash_probe_requires_hash_option() -> None:
    result = CliRunner().invoke(main, ["hash-probe"])

    assert result.exit_code == 2
    assert "Missing option '-H' / '--hash'" in result.output
