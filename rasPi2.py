#!/usr/bin/env python3

import sys, socket, time

def raw_line_to_responsecode(rawLine):
    result = rawLine

    return result

RPL_NAMREPLY = '353'    # irc status modes
RPL_ENDOFNAMES = '366'  # tells when certain operations have been completed

irc = {
    'host' : 'irc.libera.chat',  # Fully qualified domain name of irc server
    'port' : 6667,
    'channel' : '#jim',
    'namesinterval' : 15
}

user = {
    'nick' : 'jm-bot',                   # use nick-bot
    'username' : 'botuser',               # username-bot
    'hostname' : 'localhost',
    'servername' : 'irc.libera.chat',
    'realname' : 'Raspberry Pi Names Bot' # add a descriptive message
}

'''
class socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
Create a socket object.  AF_INET is the address family (the default).
SOCK_STREAM is the socket type (the default).
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print( 'Connecting to %(host)s:%(port)s...' % irc)
try:
    s.connect((irc['host'], irc['port']))
except socket.error as se:
    print( 'Error connecting to IRC server %(host)s:%(port)s') % irc
    print( se)
    sys.exit(1)

print("connect succeeded")

#exit()

#s.send('NICK %(nick)s\r\n'.encode() % user)
encodedNick = ('NICK %(nick)s\r\n' % user).encode()
s.send(encodedNick)
print('sent NICK %(nick)s\r\n' % user)
s.send(('USER %(username)s %(hostname)s %(servername)s :%(realname)s\r\n' % user).encode())
print('sent USER %(username)s %(hostname)s %(servername)s :%(realname)s\r\n' % user)
s.send(('JOIN %(channel)s\r\n' % irc).encode())
print('sent JOIN %(channel)s\r\n' % irc)
s.send(('NAMES %(channel)s\r\n' % irc).encode())
print('sent NAMES %(channel)s\r\n' % irc)

read_buffer = ''
names = []

while True:
    read_buffer += (s.recv(1024).decode())
    print("read next 1024")
    lines = read_buffer.split('\r\n')
    read_buffer = lines.pop();     # that semicolon is in both copies of code
    for line in lines:
        print('for line in lines')
        response = line.rstrip().split(' ', 3)
        response_code = response[1]
        print( 'response code is ' + str(response_code) )
        if response_code == RPL_NAMREPLY:
            print('resp. was RPL_NAMREPLY')
            names_list = response[3].split(':')[1]
            names += names_list.split(' ')
        if response_code == RPL_ENDOFNAMES:
            # Display the names
            print('resp. was RPL_ENDOFNAMES')
            print( '\r\nUsers in %(channel)s:' % irc)
            for name in names:
                print(name)
            names = []
            time.sleep(irc['namesinterval'])
            s.send(('NAMES %(channel)s\r\n' % irc).encode())
