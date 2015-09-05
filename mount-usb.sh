#!/bin/bash
# stop the GETTY service if needed
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
fstr=${fstr:1} # strip leading comma
rostr=${rostr:1} # strip leading comma
echo "$fstr" >/tmp/usbexports # save for later r/w export

# now export it
vend=$(( 0x1337 )) # pick your favorite vid/pid
prod=$(( 0x1337 ))
echo "$vend" >/tmp/usbvend # save vid/pid for r/w export
echo "$prod" >/tmp/usbprod
modprobe g_multi file=$fstr cdrom=0 stall=0 ro=$rostr \
  removable=1 nofua=1 idVendor=$vend idProduct=$prod
