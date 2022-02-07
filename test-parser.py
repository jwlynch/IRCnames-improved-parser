from irc_line_parser import raw_line_parse

f = open("little-raw-log.txt", "r")

for line in f:
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    print(f"parsed: {repr(raw_line_parse(line))}")
    # the line without return/linefeed at the end (rstrip takes them out)
    line_no_crlf = line.rstrip()

    # print adds its own crlf at the end of what it's printing
    print(f"the line: {line_no_crlf}")

print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
