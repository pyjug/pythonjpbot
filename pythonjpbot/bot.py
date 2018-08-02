import io
import traceback
import discord

from . import botcmd, quote, reaction

client = discord.Client()


def send_exp(channel):
    s = io.StringIO()
    traceback.print_exc(file=s)
    print(s.getvalue())
    client.loop.create_task(client.send_message(channel, s.getvalue()))


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
        send_exp(msg.channel)


def my_parse_message_reaction_add(self, data):
    '''{'user_id': '370411922920833024', 'message_id': '473333106758254622',
    'emoji': {'name': 'guido', 'id': '467217552016408579', 'animated': False},
    'channel_id': '411079445927952389', 'guild_id': '411079445927952385'}'''

    channel = None
    try:
        channel = self.get_channel(data['channel_id'])
        if not channel:
            return
        user = self._get_member(channel, data['user_id'])
        if not user:
            return

        f = client.loop.create_task(
            client.get_message(channel, data['message_id']))

        def done(f):
            try:
                msg = f.result()
                reaction.on_reaction(client, channel, user, msg, data)

            except Exception as e:
                traceback.print_exc()
                print("Error:", e)


        f.add_done_callback(done)
        

    except Exception:
        if channel:
            send_exp(channel)
        else:
            traceback.print_exc()

#    emoji = data.get('emoji', None)
#    if not emoji:
#        return
#    if emoji:


def run(key):
    def f(data): return my_parse_message_reaction_add(client.connection, data)
    client.connection.parse_message_reaction_add = f
    client.run(key)
