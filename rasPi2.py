#!/usr/bin/env python3

import sys, socket, time

def raw_line_to_responsecode(rawLine):
    result = rawLine

    return result

RPL_NAMREPLY = '353'    # irc status modes
RPL_ENDOFNAMES = '366'  # tells when certain operations have been completed

response_dict = {}

response_dict["001"] = "RPL_WELCOME"
response_dict["002"] = "RPL_YOURHOST"
response_dict["003"] = "RPL_CREATED"
response_dict["004"] = "RPL_MYINFO"
response_dict["005"] = "RPL_BOUNCE"

response_dict["200"] = "RPL_TRACELINK"
response_dict["201"] = "RPL_TRACECONNECTING"
response_dict["202"] = "RPL_TRACEHANDSHAKE "
response_dict["203"] = "RPL_TRACEUNKNOWN"
response_dict["204"] = "RPL_TRACEOPERATOR"
response_dict["205"] = "RPL_TRACEUSER"
response_dict["206"] = "RPL_TRACESERVER"
response_dict["207"] = "RPL_TRACESERVICE"
response_dict["208"] = "RPL_TRACENEWTYPE"
response_dict["209"] = "RPL_TRACECLASS"
response_dict["210"] = "RPL_TRACERECONNECT"
response_dict["211"] = "RPL_STATSLINKINFO"
response_dict["212"] = "RPL_STATSCOMMANDS"
response_dict["219"] = "RPL_ENDOFSTATS"
response_dict["221"] = "RPL_UMODEIS"
response_dict["234"] = "RPL_SERVLIST"
response_dict["235"] = "RPL_SERVLISTEND"
response_dict["242"] = "RPL_STATSUPTIME"
response_dict["243"] = "RPL_STATSOLINE"
response_dict["251"] = "RPL_LUSERCLIENT"
response_dict["252"] = "RPL_LUSEROP"
response_dict["253"] = "RPL_LUSERUNKNOWN"
response_dict["254"] = "RPL_LUSERCHANNELS"
response_dict["255"] = "RPL_LUSERME"
response_dict["256"] = "RPL_ADMINME"
response_dict["257"] = "RPL_ADMINLOC1"
response_dict["258"] = "RPL_ADMINLOC2"
response_dict["259"] = "RPL_ADMINEMAIL"
response_dict["261"] = "RPL_TRACELOG"
response_dict["262"] = "RPL_TRACEEND"
response_dict["263"] = "RPL_TRYAGAIN"
response_dict["301"] = "RPL_AWAY"
response_dict["302"] = "RPL_USERHOST"
response_dict["303"] = "RPL_ISON"
response_dict["305"] = "RPL_UNAWAY"
response_dict["306"] = "RPL_NOWAWAY"
response_dict["311"] = "RPL_WHOISUSER"
response_dict["312"] = "RPL_WHOISSERVER"
response_dict["313"] = "RPL_WHOISOPERATOR"
response_dict["314"] = "RPL_WHOWASUSER"
response_dict["315"] = "RPL_ENDOFWHO"
response_dict["317"] = "RPL_WHOISIDLE"
response_dict["318"] = "RPL_ENDOFWHOIS"
response_dict["319"] = "RPL_WHOISCHANNELS"
response_dict["321"] = "RPL_LISTSTART"
response_dict["322"] = "RPL_LIST"
response_dict["323"] = "RPL_LISTEND"
response_dict["324"] = "RPL_CHANNELMODEIS"
response_dict["325"] = "RPL_UNIQOPIS"
response_dict["331"] = "RPL_NOTOPIC"
response_dict["332"] = "RPL_TOPIC"
response_dict["341"] = "RPL_INVITING"
response_dict["342"] = "RPL_SUMMONING"
response_dict["346"] = "RPL_INVITELIST"
response_dict["347"] = "RPL_ENDOFINVITELIST"
response_dict["348"] = "RPL_EXCEPTLIST"
response_dict["349"] = "RPL_ENDOFEXCEPTLIST"
response_dict["351"] = "RPL_VERSION"
response_dict["352"] = "RPL_WHOREPLY"
response_dict["353"] = "RPL_NAMREPLY"
response_dict["364"] = "RPL_LINKS"
response_dict["365"] = "RPL_ENDOFLINKS"
response_dict["366"] = "RPL_ENDOFNAMES"
response_dict["367"] = "RPL_BANLIST"
response_dict["368"] = "RPL_ENDOFBANLIST"
response_dict["369"] = "RPL_ENDOFWHOWAS"

response_dict["371"] = "RPL_INFO"
response_dict["372"] = "RPL_MOTD"
response_dict["374"] = "RPL_ENDOFINFO"
response_dict["375"] = "RPL_MOTDSTART"
response_dict["376"] = "RPL_ENDOFMOTD"
response_dict["381"] = "RPL_YOUREOPER"
response_dict["382"] = "RPL_REHASHING"
response_dict["383"] = "RPL_YOURESERVICE"
response_dict["391"] = "RPL_TIME"
response_dict["392"] = "RPL_USERSSTART"
response_dict["393"] = "RPL_USERS"
response_dict["394"] = "RPL_ENDOFUSERS"
response_dict["395"] = "RPL_NOUSERS"

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
