import urllib

from sqlalchemy import create_engine

from commands import BaskCommands
from db import BaseModel, Session
from decorators import cache
from models import CommandModel


class BaskServer(object):
    FALLBACK_URL = "http://google.com/search?q="

    def __init__(self, db='bask.db', commands=None):
        self.db = create_engine("sqlite:///%s" % db)
        BaseModel.metadata.create_all(self.db)
        Session.configure(bind=self.db)

        self.commands = commands or BaskCommands()

    def process(self, query, args):
        return self.commands.build_url(query, args) or\
            self._build_url_from_db(query, args) or\
            self._build_fallback_url(query, args)

    def _build_url_from_db(self, query, args):
        url = self._url_from_db(query)
        if url is None:
            return None

        return self._build_url(url, args)

    def _build_fallback_url(self, query, args):
        args = [query] + args
        return self._build_url(self.FALLBACK_URL, args)

    def _build_url(self, url, args):
        query_string = ' '.join(args)
        quoted_query_string = urllib.quote(query_string)
        return url + quoted_query_string

    @cache
    def _url_from_db(self, query):
        matching_keys = []

        session = Session()
        qry = session.query(CommandModel).filter(CommandModel.name == query)
        for row in qry:
            matching_keys.append(row)

        return matching_keys[0] if matching_keys else None
