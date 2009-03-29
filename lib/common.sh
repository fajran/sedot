
PATH=$BASE/bin:$PATH

do_lock () {
	LOCK=$1
	
	RES=1

	exec 4>&2
	exec 2>/dev/null
	set -o noclobber
	if date -R > $LOCK ; then
		RES=0
	fi
	set +o noclobber
	exec 2>&4

	return $RES
}

do_unlock () {
	LOCK=$1
	
	rm -f $LOCK 2> /dev/null
}

get_url () {
	PKG=$1
	PROTOCOL=$2

	FURL=$BASE/pkgs/$PKG/url
	[ -f $FURL ] || return 1
	
	if [ "$PROTOCOL" == "rsync" ]; then
		grep '^rsync:\/\/\|^[^:]\+::' $FURL | sed 's/\([^:]\+\)::/rsync:\/\/\1\//'
	elif [ "$PROTOCOL" != "" ]; then
		grep "^$PROTOCOL:\/\/" $FURL
	else
		cat $FURL
	fi
}


get_color () {
	exec 2> /dev/null

	PKG=$1

	FCOLOR=$BASE/pkgs/$PKG/color
	if [ ! -f $FCOLOR ]; then
		echo $DEFAULT_COLOR
	else
		cat $FCOLOR | sed 's/#//g'
	fi
}

echo_error () {
	echo "$*" >&2
}

get_content () {
	exec 2> /dev/null

	FILE=$1
	echo "`grep -v '^\s*#' $FILE`"
}

get_value () {
	FILE=$1
	echo "`get_content $FILE | head -n1`"
}

get_rsync_source () {
	exec 2> /dev/null

	PKG=$1
	sed 's/rsync:\/\/\([^/]\+\)\//\1::/' $PKG
}


