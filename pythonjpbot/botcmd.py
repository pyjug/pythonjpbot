import shlex
import argparse
import io
import sys
import re

from google.cloud import datastore

# export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
datastore_client = datastore.Client()

# hack argparse
_org_sys = argparse._sys


class _dummy:
    def write(*args, **kwargs):
        pass


_dummy_file = _dummy()


class _proxy:
    def __getattr__(self, name):
        if name in ('stdout', 'stderr'):
            return _dummy_file
        return getattr(_org_sys, name)


argparse._sys = _proxy()


parser = argparse.ArgumentParser(
    prog='/bot',
    description='PythonJP Discord bot',
    add_help=False)

parser.add_argument('-h', '--help', help='Show help', action='store_const', const=True)


parser.exit = lambda *args: None

subparsers = parser.add_subparsers(help='sub-command help', dest='resp')

reply = subparsers.add_parser('resp', help='Manage auto response', add_help=False)

reply.add_argument('--help', action='store_const', dest='resp_help',
                   const=True, default=False, help="Remove WORD")

reply.add_argument('--remove', dest='resp_remove', action='store_const',
                   const=True, default=False, help="Remove WORD")

reply.add_argument('--list', dest='resp_list', action='store_const',
                   const=True, default=False, help="List RESPONSES")

reply.add_argument('resp_word', metavar='WORD', help="When someone says:", nargs='?', default='')
reply.add_argument('resp_reply', metavar='RESPONSE', help="I response:", nargs='?', default='')


def get_help(args):
    s = io.StringIO()
    args.print_help(s)
    return s.getvalue()


async def run(client, msg):

    k = datastore_client.key('AUTORESP', msg.content.strip())
    ret = datastore_client.get(k)
    if ret:
        await client.send_message(msg.channel, ret['resp'])
        return True

    if not re.match(r'^/bot\b', msg.content):
        return False

    command = shlex.split(msg.content)[1:]
    try:
        args = parser.parse_args(command)
    except TypeError:
        await client.send_message(msg.channel, get_help(parser))
        return True

    if not command or args.help:
        await client.send_message(msg.channel, get_help(parser))
        return True

    if getattr(args, 'resp', False):
        if args.resp_help:
            await client.send_message(msg.channel, get_help(reply))
        elif args.resp_list:
            query = datastore_client.query(kind='AUTORESP')
            for e in query.fetch():
                s = f'{e.key.name} →  {e["resp"]}'
                await client.send_message(msg.channel, s)

        elif args.resp_remove:
            word = args.resp_word.strip()
            key = datastore_client.key('AUTORESP', word)
            datastore_client.delete(key)

        else:
            word = args.resp_word.strip()
            replyword = args.resp_reply.rstrip()
            if not word or not replyword:
                await client.send_message(msg.channel, get_help(reply))
                return

            resp = datastore.Entity(key=datastore_client.key('AUTORESP', word))
            resp['resp'] = replyword
            datastore_client.put(resp)

        return True
