class Shell(object):
    def __init__(self, args):
        self.type = args.type
        self.user = args.user
        self.password = args.password
        self.host = args.host
        self.port = args.port

    def run(self):
        raise NotImplementedError('Abstract method not implemented.')
