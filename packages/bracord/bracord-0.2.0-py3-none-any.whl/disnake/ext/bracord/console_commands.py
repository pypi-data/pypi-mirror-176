"""
This file stores the different CLI commands.
"""

import os
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt

from disnake.ext.bracord.boilerplate import cog_boilerplate
from disnake.ext.bracord.project_init import init_base_project

console = Console()


def cog():
    """Command that runs when `bracord cog` is ran."""

    # TODO: Regex to check a valid class name.
    cog_name = Prompt.ask("[bold bright_yellow]Enter the name of your cog")

    with open(f"./{cog_name}.py", encoding="utf-8", mode="w") as f:
        f.write(cog_boilerplate.format(cog_name=cog_name))

    console.print(f"[bold bright green]Successfully created {cog_name}.py")


def init_project():
    """Command that runs when `bracord init` is ran."""
    bot_name = Prompt.ask("[bold bright_yellow]Enter the name of your bot")
    bot_token = Prompt.ask("[bold bright_yellow]Enter your bot's token")
    bot_version = Prompt.ask(
        "[bold bright_yellow]Enter the version of your bot", default="0.1.0"
    )

    use_slash = Confirm.ask(
        "[bold bright_yellow]Do you want to use Slash Commands only?"
    )

    bot_prefix = None
    if not use_slash:
        bot_prefix = Prompt.ask("[bold bright_yellow]Enter your bot's command prefix")

    test_guild_id = IntPrompt.ask(
        "[bold bright_yellow]Enter the ID of your bot's test server (leave this empty to set it up later)",
        show_default=None,
        default="",
    )

    init_base_project(
        use_slash=use_slash,
        bot_name=bot_name,
        bot_token=bot_token,
        bot_version=bot_version,
        test_guild_id=test_guild_id,
        bot_prefix=bot_prefix,
    )
