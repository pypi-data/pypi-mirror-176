import os
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt

from disnake.ext.bracord.boilerplate import (
    cog_boilerplate,
    interaction_bot_boilerplate,
    message_bot_boilerplate,
)

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
    use_slash = Confirm.ask(
        "[bold bright_yellow]Do you want to use Slash Commands only?"
    )
    bot_name = Prompt.ask("[bold bright_yellow]Enter the name of your bot")
    bot_token = Prompt.ask("[bold bright_yellow]Enter your bot's token")
    bot_version = Prompt.ask(
        "[bold bright_yellow]Enter the version of your bot", default="0.1.0"
    )
    test_guild_id = IntPrompt.ask(
        "[bold bright_yellow]Enter the ID of your bot's test server (leave this empty to set it up later)",
        show_default=None,
        default="",
    )

    if use_slash:
        console.print("[bold bright_blue]Creating bot structure...")

        bot_folder = bot_name.lower().replace(" ", "_")
        os.mkdir(f"./{bot_folder}")

        with open("./.env", encoding="utf-8", mode="w") as f:
            f.write(
                f"""BOT_NAME = "{bot_name}"
BOT_TOKEN = "{bot_token}"
BOT_VERSION = "{bot_version}"

"""
            )

        with open("./bot.py", encoding="utf-8", mode="w") as f:
            f.write(
                f"""from {bot_folder} import bot, BOT_TOKEN

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
"""
            )

        with open(f"./{bot_folder}/__init__.py", encoding="utf-8", mode="w") as f:
            bot_code = interaction_bot_boilerplate.replace(
                "//test_guild_id//", str(test_guild_id)
            )
            f.write(bot_code)
