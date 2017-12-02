#!/usr/bin/python
import sys
import MockSSH

#
# command: pwd
#
def pwd_command_success(instance):
    instance.writeln("[OK]")

def pwd_command_failure(instance):
    instance.writeln("MockSSH: Supported usage: pwd")

command_pwd = MockSSH.ArgumentValidatingCommand('pwd', [pwd_command_success],
                                               [pwd_command_failure], *[])

commands = [ command_pwd ]

def main():
    users = {'testadmin': 'x'}
    MockSSH.runServer(
        commands, prompt="hostname>", interface='127.0.0.1', port=9999, **users)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "User interrupted"
        sys.exit(1)
