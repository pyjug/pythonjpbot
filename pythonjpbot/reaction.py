import re
import json
import zlib

import discord
from google.cloud import datastore
from . datastore import datastore_client


async def on_reaction(client, payload): #client, channel, user, msg, data):
    #    'emoji': {'name': 'guido', 'id': '467217552016408579', 'animated': False},

    channel = client.get_channel(payload.channel_id)
    if not channel:
        return

    msg = await channel.fetch_message(payload.message_id)
    if not msg:
        return

    name = payload.emoji.name
    id = payload.emoji.id

    if id:
        s = [name, id]
    else:
        s = [name, None]

    k = datastore_client.key('USERREACTION', str(msg.author.id))
    ret = datastore_client.get(k)

    if ret:
        d = json.loads(zlib.decompress(ret['rc']))
    else:
        d = []

    updated = []
    seen = False

    n = 1
    for emoji, v in d:
        if emoji == s:
            n = v + 1
            seen = True
        else:
            updated.append((emoji, v))

    updated.insert(0, (s, n))

    e = datastore.Entity(key=k, exclude_from_indexes=['rc'])
    e['rc'] = zlib.compress(json.dumps(updated).encode('utf-8'))
    datastore_client.put(e)


async def show(client, msg):

    c = msg.content.rstrip()
    m = re.match(r'^/reaction\s*(<@!?(\d{18})>)?$', c)
    if not m:
        return

    if not m.group(2):
        userid = str(msg.author.id)
    else:
        userid = m[2]

    k = datastore_client.key('USERREACTION', userid)
    ret = datastore_client.get(k)

    s = []
    if ret:
        d = json.loads(zlib.decompress(ret['rc']))
        emojis = {e.id for e in msg.guild.emojis}

        for (name, id), v in d:
            if id:
                if not id in emojis:  # ignore external/unknown emoji
                    continue
                name = f"<:{name}:{id}>"

            s.append(f'{name}: {v}')
        if s:
            await msg.channel.send( ','.join(s))
            return True

    await msg.channel.send('No reactions...')

    return True
