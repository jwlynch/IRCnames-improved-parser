def raw_line_parse(line):
    # Here, we have one line in the var line, so now, let's pull
    # it apart and build a dict with everything we find.

    # pull off tags and origin words from line
    lineDict = {}

    # separate lines into "words" (things between spaces)
    llist = line.split(" ")

    # within the line parser, when looking at llist,
    # the first (leftmost) 'word' might start with a @
    # if it does, it's a "tags" word, so we pull it out
    # of the llist, save it, and indicate we found it.
    #
    # same thing, for a word starting with :, this is called
    # a 'prefix'.
    #
    # a line can have 0 or 1 "tags" word, and 0 or 1 "prefix" word
    tags_p = False
    prefix_p = False

    if llist[0].startswith('@'):
        tagWord = llist.pop(0)
        tags_p = True
        lineDict["tags"] = tagWord[1:] # all but the @

    if llist[0].startswith(":"):
        prefixWord = llist.pop(0)
        prefix_p = True
        lineDict["prefix"] = prefixWord[1:] # all but the :

    # we've taken out the tags word and the prefix from the llist.
    #
    # Now, the leftmost word in llist is the command (aka response_code)

    # now, llist[0] is the command (used to call it response_code)
    commandWord = llist.pop(0)
    lineDict["command"] = commandWord

    # we've taken out a tags word, a prefix (if either exists), and
    # the command. what we're left with, is args.

    # I'll comment the arg parser later.

    # (next, parse args... let's see what's there)
    colonlastarg_p = False
    arglist = []
    lastarglist = []
    mode = "singleArgs"
    for arg in llist:
        if mode == "singleArgs":
            if arg.startswith(":"):
                firstOfLastArg = arg[1:]
                lastarglist.append(firstOfLastArg)
                mode = "lastarg"
                colonlastarg_p = True
            else:
                if mode == "singleArgs":
                    arglist.append(arg)
                else:
                    lastarglist.append(arg)
        else:
            lastarglist.append(arg)

    if colonlastarg_p:
        lastarg = " ".join(lastarglist)
        arglist.append(lastarg)

    lineDict["args"] = arglist

    # Here, we are done looking at the line, and have a fully
    # formed dict (in var lineDict) with all the info from the line
    # so, below this point, we could use just the lineDict

    result = lineDict

    return result

