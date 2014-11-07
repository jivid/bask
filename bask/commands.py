import urllib

class BaskCommands(object):
    def build_url(self, cmd, args):
        if not hasattr(self, cmd):
            return None

        func = getattr(self, cmd)
        url = "http://%s" % func(args)
        return url
