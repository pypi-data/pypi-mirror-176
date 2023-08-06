import pyshorteners

def shortier(linkURL, servProvider=None):

    if not servProvider:
        return pyshorteners.Shortener().tinyurl.short(linkURL)
    if servProvider ==  "chilpit":
        return pyshorteners.Shortener().chilpit.short(linkURL)
    if servProvider == "clckru":
        return pyshorteners.Shortener().clckru.short(linkURL)
    if servProvider == "dagd":
        return pyshorteners.Shortener().dagd.short(linkURL)
    if servProvider == "isgd":
        return pyshorteners.Shortener().isgd.short(linkURL)
    if servProvider == "osdb":
        return pyshorteners.Shortener().osdb.short(linkURL)
    if servProvider == "tinyurl":
        return pyshorteners.Shortener().tinyurl.short(linkURL)