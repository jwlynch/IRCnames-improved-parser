#!/usr/bin/env python3

import sys, socket, time

from response_codes import response_dict
from irc_line_parser import raw_line_parse

from configparser import ConfigParser
from pathlib import Path

RPL_NAMREPLY = '353'    # irc status modes
RPL_ENDOFNAMES = '366'  # tells when certain operations have been completed

# index of item in list, or -1 if ValueError
def dex(item, lst):
    result = -1

    try:
        result = lst.index(item)
    finally:
        return result

# at first, this will be each hook
debugSects = []

def debugSectsContains(sectName):
    result = dex(sectName, debugSects) != -1

    return result

# nedbat's hack to replace __file__ (used to locate this script's dir)
def foo():
    pass
pathname = Path(foo.__code__.co_filename).parent.__str__()

configFilePath = Path(pathname) / "IRCnamesBot.cfg"

def doReadConfig(path):
    parser = ConfigParser()
    result = parser.read(path)

    result_paths = [Path(p) for p in result]

    if dex(path, result_paths) == -1:
        print(f"ERROR, did not find {path} in parser output")
        exit()

    result = {}

    # overall result is a dict, populated with the section names...
    for section in parser.sections():
        # ... and each section name gets its own dict
        result[section] = {}

        # sections get populated with options, each option finally gets a value
        for opt in parser.options(section):
            # in each option, put the value of that option
            result[section][opt] = parser[section][opt]
        

    return(result)

params = doReadConfig(configFilePath)

#irc = {
#    'host' : 'irc.libera.chat',  # Fully qualified domain name of irc server
#    'port' : 6667,
#    'channel' : '#jim',
#    'namesinterval' : 15
#}

#user = {
#    'nick' : 'jm-bot',                   # use nick-bot
#    'username' : 'botuser',               # username-bot
#    'hostname' : 'localhost',
#    'servername' : 'irc.libera.chat',
#    'realname' : 'Raspberry Pi Names Bot' # add a descriptive message
#}

'''
class socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
Create a socket object.  AF_INET is the address family (the default).
SOCK_STREAM is the socket type (the default).
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print( 'Connecting to %(host)s:%(port)s...' % params["irc"])
try:
    s.connect((params["irc"]['host'], int(params["irc"]['port'])))
except socket.error as se:
    print( 'Error connecting to IRC server %(host)s:%(port)s') % params["irc"]
    print( se)
    sys.exit(1)

print("connect succeeded")

#exit()

#s.send('NICK %(nick)s\r\n'.encode() % user)
encodedNick = ('NICK %(nick)s\r\n' % params["user"]).encode()
s.send(encodedNick)
print('sent NICK %(nick)s\r\n' % params["user"])
s.send(('USER %(username)s %(hostname)s %(servername)s :%(realname)s\r\n' % params["user"]).encode())
print('sent USER %(username)s %(hostname)s %(servername)s :%(realname)s\r\n' % params["user"])
s.send(('JOIN %(channel)s\r\n' % params["irc"]).encode())
print('sent JOIN %(channel)s\r\n' % params["irc"])
#s.send(('NAMES %(channel)s\r\n' % params["irc"]).encode())
#print('sent NAMES %(channel)s\r\n' % params["irc"])

read_buffer = ''
names = []

while True:
    read_buffer += (s.recv(1024).decode())
    lines = read_buffer.split('\r\n')
    read_buffer = lines.pop();     # that semicolon is in both copies of code
    for line in lines:

        lineDict = raw_line_parse(line)

        print("line dict is " + repr(lineDict))

        # here, we get whatever's needed from the lineDict

        command = lineDict["command"]

        # print the response code according to whether that code appears
        # in the response_dict.
        if command in response_dict:
            command_label = response_dict[command]
            print( f'command is {command}, {command_label}' )
        else:
            print( f'command is {command}' )

        if command == RPL_NAMREPLY:
            nameStr = lineDict["args"][-1] # get last arg, a space-separated
                                           # string with the names on the
                                           # channel
            # print the names string
            print("RPL_NAMREPLY args: " + repr(lineDict["args"]) )
        if command == RPL_ENDOFNAMES:
            names = nameStr.split(" ") # split names into a list
            # Display the names
            print( '\r\nUsers in %(channel)s:' % params["irc"])
            for name in names:
                print(name)
            # don't do another /names
            #names = []

            # don't sleep this way, it blocks everything while sleeping
            #time.sleep(irc['namesinterval'])

            # don't do another /names
            #s.send(('NAMES %(channel)s\r\n' % irc).encode())

        # this handles server pings (which are different than those
        # we get when someone does: /ping some-nick.

        # if we get a server ping...
        if command.lower() == 'ping':
            # we want to send the args back in the "pong", so 'join' them
            ping_args = " ".join(lineDict["args"])
            pong = f"PONG {ping_args}" # this is what to send to the server
            s.send(pong.encode()) # send it

        if command.lower() == 'privmsg':
            msg_args = lineDict['args']
            msg_to = msg_args[0]
            msg = msg_args[1]
            msg_from = lineDict['prefix']
            print(f"msg to {msg_to} from {msg_from}: {msg}")
