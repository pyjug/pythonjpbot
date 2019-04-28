import io
import traceback
import discord

from . import botcmd, quote, reaction

client = discord.Client()


async def send_exp(channel):
    s = traceback.format_exc()
    print(s)
    await channel.send(s)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if not msg.content:
        return

    try:
        ret = await reaction.show(client, msg)
        if ret:
            return
        ret = await botcmd.run(client, msg)
        if ret:
            return

    except Exception:
        await send_exp(msg.channel)


@client.event
async def on_raw_reaction_add(payload):
    await reaction.on_reaction(client, payload)


def run(key):
    client.run(key)
