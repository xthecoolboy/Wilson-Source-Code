import config


owner = config.bot['owner']

def is_owner(ctx):
    return str(ctx.message.author.id) in owner