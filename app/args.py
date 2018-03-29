class Arguments(object):
    def __init__(self, args):
        self.type = args.type
        self.cmd = args.cmd
        self.user = args.user
        self.password = args.password
        self.host = args.host
        self.port = args.port

    def getType(self):
        return self.type

    def getCmd(self):
        return self.cmd.split('#')

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port
