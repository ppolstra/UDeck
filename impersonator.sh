#!/bin/bash

usage () {
  echo "Usage: $0 [-v Vendor] [-p Product] [-d Delay]"
  echo "USB impersonator shell script.  Will interate"
  echo "over list if no vendor and product id given."
  echo "Standard delay is four seconds before switching."
  exit 1
}
declare -i vend=0x1337
declare -i prod=0x1337
declare -i delay=4

parseargs () {
  useFile=true
  delay=$(( 2 ))
  while [[ $# > 1 ]]
  do
    key="$1"
    case $key in
    -v)
      vend="0x$2" 
      useFile=false
      shift
      ;;
    -p)
      prod="0x$2" 
      useFile=false
      shift
      ;;
    -d)
      delay=$(( $2 ))
      shift
      ;;
    *)
      usage
      ;;
    esac
    shift
  done
}

if which 'systemctl' ; then 
  systemctl stop serial-getty@ttyGS0.service >/dev/null
fi
# unload current composite gadget
modprobe -r g_multi
# these variables are used to export all partitions
fstr=""
rostr=""
# unmount the USB drive
for d in $(ls /dev/sd*) ; do
  if  echo "$d" | egrep '[1-9]$' >/dev/null ; then 
    umount $d
    fstr+=",$d"
    rostr+=",1"
  fi
done
fstr=${fstr:1}
rostr=${rostr:1}
echo "$fstr" >/tmp/usbexports

# store the process ID so it can be killed
echo "$BASHPID" > /tmp/impersonator-pid

# now export it
if $useFile ; then
  declare -a arr
  while read line
  do
    arr=(${line//,/ })
    v=${arr[0]}
    vend="0x$v"
    p=${arr[1]}
    prod="0x$p"
    printf '%x:%x\n' $vend $prod
    modprobe -r g_multi
    modprobe g_multi file=$fstr cdrom=0 stall=0 ro=$rostr \
      removable=1 nofua=1 idVendor=$vend idProduct=$prod
    sleep $delay
  done < 'vidpid-list'
else
  modprobe g_multi file=$fstr cdrom=0 stall=0 ro=$rostr \
    removable=1 nofua=1 idVendor=$vend idProduct=$prod
fi
