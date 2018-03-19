# pyrsh
Remote shell in python

to run in cmd you need to enter
`pyrsh.py type command user password host port`

type - connection type
    local - running cmd on the local machine
    ssh - connection via default libraries
    telnet - connect to telnet server
    paramiko - connection via libraries paramiko
command - comand for running
user - username
password - password for connect
host - host server
port - server port  
Example - `pyrsh.py pyr_ssh pwd user password localhost 22`

running unittests
local test - `./test_local.py`
paramiko test - `./test_pyrsh.py.py`
    mock server will be started
telnet test - 
    Step 1, run telnet server - `./run_telnet_server.py`
    Step 2, `./test_local.py`
