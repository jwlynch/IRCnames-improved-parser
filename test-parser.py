from irc_line_parser import raw_line_parse

f = open("little-raw-log.txt", "r")

for line in f:
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

    # the line without return/linefeed at the end (rstrip takes them out)
    line_no_crlf = line.rstrip()

    # print adds its own crlf at the end of what it's printing
    print(f"the line: {line_no_crlf}")

    # we have a line, now run the parser on that line
    line_dict =  raw_line_parse(line)
    # the parser will return a dict with everything about the line in it

    # repr() is how we turn the object into a string,
    # that looks like the object
    # (example, repr(someDict) will look approximately like:
    # "{'key': value, more keys: more values }")
    representation_of_lineDict = repr(line_dict)

    print(f"parsed: {representation_of_lineDict}")

print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
