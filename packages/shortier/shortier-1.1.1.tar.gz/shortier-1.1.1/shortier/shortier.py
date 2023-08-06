import pyshorteners

def shortier(linkURL, servProvider=None):

    # match int(input("-- Enter your choice in digits --")):
    # return pyshorteners.Shortener().tinyurl.short(linkURL)
    match servProvider:

        case "chilpit":
            return pyshorteners.Shortener().chilpit.short(linkURL)
        case "clckru":
            return pyshorteners.Shortener().clckru.short(linkURL)
        case "dagd":
            return pyshorteners.Shortener().dagd.short(linkURL)
        case "isgd":
            return pyshorteners.Shortener().isgd.short(linkURL)
        case "osdb":
            return pyshorteners.Shortener().osdb.short(linkURL)
        case "tinyurl":
            return pyshorteners.Shortener().tinyurl.short(linkURL)

    return pyshorteners.Shortener().tinyurl.short(linkURL)