#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basecheck import CheckMethod

class Arguments(CheckMethod):

    def __init__(self, args):
    	CheckMethod.__init__(self)
        self.type = args.type
        self.cmd = args.cmd
        self.user = args.user
        self.password = args.password
        self.host = args.host
        self.port = args.port
