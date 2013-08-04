#!/usr/bin/python2
import getopt
import mpd
import pylast
import random
import re
import sys

DEFAULT_QUERY_TYPE = 'albums'
DEFAULT_QUERY_RANGE = '3month'
DEFAULT_MAX_ITEMS = 20
DEFAULT_MPD_PLAYLIST = 'nicefm'
DEFAULT_MPD_MPD_HOST = '127.0.0.1'
DEFAULT_MPD_MPD_PORT = '6600'


def lastfm_popular(lastfm, username, query_type, range, max_items):
    user = lastfm.get_user(username)
    if query_type == "albums":
        items = user.get_top_albums(period=range,
                                    limit=max_items)
    elif query_type == "songs":
        items = user.get_top_tracks(period=range,
                                    limit=max_items)
    else:
        raise Exception("Invalid query type.")

    ret = []
    for t in items:
        item = t.item
        ret.append({'artist':item.artist.get_name().encode("ascii","ignore"),
                    'title': item.title.encode("ascii","ignore")})
    return ret

def mpd_find(mpd, items, query_type, duplicates):
    ret = []

    if query_type == "albums":
        field = "album"
    elif query_type == "songs":
        field = "title"
    else:
        raise Exception("Invalid query type.")

    count, func = duplicates

    if func == "random":
        def func(x):
            random.shuffle(x)
            return x
    elif func == "first":
        func = lambda(x): x
    elif func == "last":
        def func(x):
            x.reverse()
            return x
    else:
        raise Exception("Invalid duplicate resolution method (%s)." % func)

    for t in items:
        search = mpd._execute('search',['artist', t['artist'], field, t['title']])
        if count:
            search = func(search)[0:count]
        ret = ret + [i['file'] for i in search]
    return ret

def mpd_add_tracks(mpd, playlist, tracks):
    mpd._execute('playlistclear', [playlist])
    for t in tracks:
        mpd._execute('playlistadd', [playlist, t])

def help():
    print("""Usage: %s [flag_1, ..., flag_n] KEY SECRET USERNAME
\tFlags:
\t\t-t <type>  type = (albums | songs)

\t  -- Last.FM --
\t\t-r <range> range = (overall | 7day | 1month | 3month | 6month | 12month)
\t\t-i <max_items>

\t  -- MPD --
\t\t-m <host:port>
\t\t-p <playlist>
\t\t-d <duplicates> = [0-9]+(random | first | last)
          """ % sys.argv[0])

def parse_args(argv):
    args = []
    ret = {}
    ret['range'] = DEFAULT_QUERY_RANGE
    ret['max_items'] = DEFAULT_MAX_ITEMS
    ret['query_type'] = DEFAULT_QUERY_TYPE

    ret['mpd_playlist'] = DEFAULT_MPD_PLAYLIST
    ret['mpd_host'] = DEFAULT_MPD_MPD_HOST
    ret['mpd_port'] = DEFAULT_MPD_MPD_PORT

    while argv:
        optlist, argv = getopt.getopt(argv, 't:r:i:p:m:d:h')
        if argv:
            args.append(argv[0])
            argv = argv[1:]

        for (opt, val) in optlist:
            if opt == '-t':
                ret['query_type'] = val
            elif opt == '-r':
                ret['range'] = val
            elif opt == '-i':
                ret['max_items'] = val
            elif opt == '-p':
                ret['mpd_playlist'] = val
            elif opt == '-m':
                ret['mpd_host'], ret['mpd_port'] = val.split(':')
            elif opt == '-d':
                m = re.match('([0-9]+)((?:random|first|last))', val)
                ret['mpd_duplicates'] = [int(m.group(1)), m.group(2)]
            else:
                return None

    if len(args) != 3:
        return None

    ret['lastfm_key'], ret['lastfm_secret'], ret['lastfm_username'] = args
    return ret


def main():
    args = parse_args(sys.argv[1:])
    if not args:
        help()
        sys.exit(1)

    print args

    lastfm_conn = pylast.LastFMNetwork(api_key = args['lastfm_key'],
                                       api_secret = args['lastfm_secret'])
    popular_stuff = lastfm_popular(lastfm_conn,
                                   args['lastfm_username'],
                                   args['query_type'],
                                   args['range'],
                                   args['max_items'])

    mpd_conn = mpd.MPDClient()
    mpd_conn.connect(args['mpd_host'],
                     args['mpd_port'])

    mpd_paths = mpd_find(mpd_conn,
                         popular_stuff,
                         args['query_type'],
                         args['mpd_duplicates'])

    mpd_add_tracks(mpd_conn,
                   args['mpd_playlist'], mpd_paths)

if __name__ == "__main__":
    main()
