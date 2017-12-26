#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CheckMethod(object):

    def run(self):
        raise NotImplementedError('Determine the run in %s.' % (self.__class__.__name__))
