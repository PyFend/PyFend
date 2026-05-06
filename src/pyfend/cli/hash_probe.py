import os
from datetime import datetime
from pathlib import Path

import click
import questionary

from pyfend.tools.hashprobe.hash_probe import crack
from pyfend.tools.hashprobe.types import Info


def _validate_date(value: str) -> bool | str:
    if not value:
        return True
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return "Invalid date format, use YYYY-MM-DD"


def _get_user_info() -> Info | None:
    click.echo("[*] Enter personal info to generate a smart wordlist.")
    click.echo("    (Press Enter to skip any field)\n")

    answers = questionary.form(
        name=questionary.text("  Name :", default=""),
        nickname=questionary.text("  Nickname :", default=""),
        birth=questionary.text(
            "  Birth date (YYYY-MM-DD) :",
            default="",
            validate=_validate_date,
        ),
        extra=questionary.text("  Extra info :", default=""),
    ).ask()

    if not answers:
        return None

    birth = (
        datetime.strptime(answers["birth"], "%Y-%m-%d")
        if answers["birth"]
        else None
    )

    return Info(
        name=answers["name"],
        nickname=answers["nickname"],
        birth=birth,
        extra=answers["extra"],
    )


def _validate_wordlist(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> str | None:
    if value is not None and not Path(value).exists():
        raise click.BadParameter(
            f"Wordlist file '{value}' not found.", ctx=ctx, param=param
        )
    return value


@click.command("hash-probe")
@click.option(
    "-H",
    "--hash",
    "hash_value",
    required=True,
    metavar="HASH",
    help="Hash value to analyze.",
)
@click.option(
    "-b",
    "--bruteforce",
    default=None,
    metavar="WORDLIST",
    callback=_validate_wordlist,
    help="Path to wordlist for dictionary-based attack.",
)
@click.option(
    "--threads",
    type=int,
    default=os.cpu_count() or 4,
    show_default=True,
    help="Number of threads for dictionary testing.",
)
@click.option(
    "--limit",
    type=int,
    default=1,
    show_default=True,
    help="Limit number of crack attempts.",
)
@click.option(
    "-i",
    "--info",
    "use_info",
    is_flag=True,
    default=False,
    help="Interactively input personal info to generate a smart wordlist.",
)
def hash_probe_cmd(
    hash_value: str,
    bruteforce: str | None,
    threads: int,
    limit: int,
    use_info: bool,
) -> None:
    """Analyze and crack hashes using dictionary-based attacks.

    \b
    Examples:
      pyfend hash-probe -H 5f4dcc3b5aa765d61d8327deb882cf99
      pyfend hash-probe -H <hash> -b rockyou.txt --threads 8
      pyfend hash-probe -H <hash> -b rockyou.txt -i
    """
    info_input: Info | None = None

    if use_info:
        info_input = _get_user_info()
        if info_input is None:
            return

    try:
        crack(
            hash_value=hash_value,
            bruteforce=bruteforce,
            info=info_input,
            threads=threads,
            limit=limit,
        )
    except Exception as e:
        click.echo(f"\nError during execution: {e}", err=True)
