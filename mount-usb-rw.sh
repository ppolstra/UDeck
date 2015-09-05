#!/bin/bash
# these variables are used to export all partitions
if [ -e /tmp/usbexports ] ; then
  fstr=$(cat /tmp/usbexports)
  modprobe -r g_multi
  modprobe g_multi file=$fstr cdrom=0 stall=0 \
    removable=1 nofua=1 idVendor=$(cat /tmp/usbvend) \
    idProduct=$(cat /tmp/usbprod)
fi

