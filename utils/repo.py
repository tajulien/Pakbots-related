from utils import default

version = "v2.0.0"
invite = "https://discord.gg/cyVpKHb"
owners = default.get("config.json").owners


def is_owner(ctx):
    return ctx.author.id in owners
