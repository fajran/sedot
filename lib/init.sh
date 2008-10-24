
BASE=$( cd `dirname $0`/../; pwd )
HOST=`hostname -f`

. $BASE/etc/config.sh

[ -f $BASE/etc/conf.d/$HOST.conf ] && . $BASE/etc/conf.d/$HOST.conf


