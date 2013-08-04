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
