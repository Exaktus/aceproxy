import config.sort


def sortPlaylist(items):
    if config.sort.orderby == 'none':
        return items
    else:
        if config.sort.orderby == 'name':
            g = lambda itm: itm.name
        if config.sort.orderby == 'tvg-id':
            g = lambda itm: itm.tvgid
        if config.sort.orderby == 'tvg-name':
            g = lambda itm: itm.tvgname
        if config.sort.orderby == 'group':
            g = lambda itm: itm.grouptitle
        return sorted(items, key=g)