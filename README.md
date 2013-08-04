nicefm
======

A script that checks on last.fm the top tracks/albums/artists of a particular user and adds them to a mpd playlist.

```
Usage: nicefm.py [flag_1, ..., flag_n] KEY SECRET USERNAME
        Flags:
                -t <type>  type = (albums | songs)

          -- Last.FM --
                -r <range> range = (overall | 7day | 1month | 3month | 6month | 12month)
                -i <max_items>

          -- MPD --
                -m <host:port>
                -p <playlist>
                -d <duplicates> = [0-9]+(random | first | last)
```

Example
=====

Let's say we want to copy the 20 most listened albums in the last 7 days to some cellphone's music directory located in "/run/media/nc/139B-FDFD/Music/".

```
 $ nicefm.py $LASTFM_KEY $LASTFM_SECRET $LASTFM_USERNAME -t albums -i 20 -r 3month
 $ ./sync.sh /run/media/nc/139B-FDFD/Music/
```

Boom... done...

Dependencies
=====
 * nicefm:
    * python2
    * python-mpd
	* pylast (included due to a small hack in the lib)
 * sync.sh:
    * rsync

