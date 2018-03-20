class Arguments(object):
    def __init__(self, args, password):
        self.type = args.type
        self.cmd = args.cmd
        self.user = args.user
        self.password = password
        self.host = args.host
        self.port = args.port
