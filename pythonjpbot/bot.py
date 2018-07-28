import io
import traceback
import discord

from . import botcmd, quote

client = discord.Client()

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if not msg.content:
        return

    try:
        ret = await botcmd.run(client, msg)
        if ret:
            return

        ret = await quote.run(client, msg)
        if ret:
            return

    except Exception:
        s = io.StringIO()
        traceback.print_exc(file=s)
        await client.send_message(msg.channel, s.getvalue())

def run(key):
    client.run(key)
