import os
from datetime import datetime
from pathlib import Path

import click

from pyfend.tools.hashprobe import crack
from pyfend.tools.hashprobe.types import Info


def _validate_date(
    ctx: click.Context, param: click.Parameter, value: str | None
) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise click.BadParameter(
            "Invalid date format, use YYYY-MM-DD", ctx=ctx, param=param
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
    default=os.cpu_count(),
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
@click.pass_context
def hash_probe_cmd(
    ctx: click.Context,
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
        click.echo("[*] Enter personal info to generate a smart wordlist.")
        click.echo("    (Press Enter to skip any field)\n")

        name = click.prompt("  Name", default="", show_default=False)
        nickname = click.prompt("  Nickname", default="", show_default=False)

        birth_str = click.prompt(
            "  Birth date (YYYY-MM-DD)", default="", show_default=False
        )
        birth = _validate_date(ctx, None, birth_str or None)

        extra = click.prompt("  Extra info", default="", show_default=False)

        info_input = Info(
            name=name,
            nickname=nickname,
            birth=birth,
            extra=extra,
        )

    crack(
        hash_value=hash_value,
        bruteforce=bruteforce,
        info=info_input,
        threads=threads,
        limit=limit,
    )
