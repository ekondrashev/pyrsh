from shell import Shell

class Arguments(Shell):
    def __init__(self, args):
        self.type = args.type
        self.cmds = args.cmd.split('#')
        self.user = args.user
        self.password = args.password
        self.host = args.host
        self.port = args.port
        self.result = {}
