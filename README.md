# IRCnames

This version is derived from the one John Cassady did, that said,
I changed a lot.

I added a complete irc raw line parser, tried to make sure the other
code used data produced by that parser, and also added a section that
responds to server pings, by looking at the arguments sent with the
ping, and sending those arguments back, in a "pong". Result being, the
bot announces to the server, that it's still alive, and so never gets
disconnected by the server for inactivity.

I added comments so that the reader can understand where the parser
begins and ends, and it also prints the output of the server, which
is a dict containing all details of the line.
