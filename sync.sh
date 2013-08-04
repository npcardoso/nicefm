#!/bin/bash
if [[ $# == 1 ]]; then
	DEST=$1;
else
	echo "Usage: $0 [Dest]" >&2 
	exit 1
fi

if [[ -z $CONF_NICE_FM_MPD_PLAYLIST ]]; then
	PLAYLIST="nicefm"
	echo "\$CONF_NICE_FM_MPD_PLAYLIST not set! Using '$PLAYLIST'"
else
	PLAYLIST=$CONF_NICE_FM_MPD_PLAYLIST
fi

if [[ -z $CONF_NICE_FM_ROOT ]]; then
	ROOT_DIR=$(cat /etc/mpd.conf |grep "music_directory" | grep -v ' *#' | sed 's/.*"\(.*\)".*/\1/')
	echo "\$CONF_NICE_FM_ROOT not set! Using: '$ROOT_DIR'"
else
	ROOT_DIR=$CONF_NICE_FM_ROOT
fi

if [[ -z $CONF_NICE_FM_PLAYLIST_ROOT ]]; then
	PLAYLIST_ROOT_DIR=$(cat /etc/mpd.conf |grep "playlist_directory" | grep -v ' *#' | sed 's/.*"\(.*\)".*/\1/')
	echo "\$CONF_NICE_FM_PLAYLIST_ROOT not set! Using: '$PLAYLIST_ROOT_DIR'"
else
	PLAYLIST_ROOT_DIR=$CONF_NICE_FM_PLAYLIST_ROOT
fi

command rsync -a --compress-level=0 -Pv -x --files-from=$PLAYLIST_ROOT_DIR/$PLAYLIST.m3u $ROOT_DIR $DEST
