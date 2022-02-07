from irc_line_parser import raw_line_parse

f = open("little-raw-log.txt", "r")

for line in f:
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"the line: {line.rstrip()}")
print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
