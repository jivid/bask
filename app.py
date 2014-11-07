import os

from bask.commands import BaskCommands
from bask.server import BaskServer
from flask import Flask, redirect, request


class Commands(BaskCommands):
    def mdn(self, args):
        mdn_base = 'developer.mozilla.org/en-US/docs/Web'
        resource = args[0]

        if resource not in ['css', 'js']:
            return mdn_base

        # Rewrite the resource name if it's js
        resource = 'javascript' if resource == 'js' else resource

        parts = [mdn_base, resource]
        if len(args) > 1:
            parts.append(args[1])

        return '/'.join(parts)

    def w(self, args):
        return 'wikipedia.com/wiki/index.php?search=' + args[0]

    def hub(self, args):
        parts = ['github.com']
        parts.append(args[0])  # first argument is user or repo

        # Check if there's a branch specified
        if len(args) > 1:
            parts = parts + ['tree', args[1]]

        return '/'.join(parts)


db = os.path.abspath('bask.db')
bask = BaskServer(db, Commands())
app = Flask('BaskServer')


@app.route('/')
def serve():
    terms = request.args.keys()[0].split()
    query, args = terms[0], terms[1:]
    url = bask.process(query, args)
    return redirect(url)

app.run(host='0.0.0.0')
