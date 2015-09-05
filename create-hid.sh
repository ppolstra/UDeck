#!/bin/bash
# This script will create a HID device on the BBB

# if the g_multi device is loaded remove it
if lsmod | grep g_multi >/dev/null ; then
  modprobe -r g_multi
fi
# check for the existance of configfs
if mount | grep '/sys/kernel/config' >/dev/null ; then
  umount /sys/kernel/config 
fi
mount none -t configfs /sys/kernel/config
# create a keyboard device
kbdir="/sys/kernel/config/usb_gadget/kb"
if [ ! -d "$kbdir" ] ; then
  mkdir $kbdir
fi
echo 0x1337 >"$kbdir/idVendor"
echo 0x1337 >"$kbdir/idProduct"
echo 0x0100 >"$kbdir/bcdDevice"
echo 0x0110 >"$kbdir/bcdUSB"
if [ ! -d "$kbdir/configs/c.1" ] ; then 
  mkdir "$kbdir/configs/c.1"
fi
echo 500 >"$kbdir/configs/c.1/MaxPower"
if [ ! -d "$kbdir/functions/hid.usb0" ] ; then
  mkdir "$kbdir/functions/hid.usb0"
fi
echo 1 >"$kbdir/functions/hid.usb0/subclass"
echo 1 >"$kbdir/functions/hid.usb0/protocol"
echo 8 >"$kbdir/functions/hid.usb0/report_length"
cp report_descriptor_kb.bin "$kbdir/functions/hid.usb0/report_desc"
ln -s "$kbdir/functions/hid.usb0" "$kbdir/configs/c.1"
echo musb-hdrc.0.auto >"$kbdir/UDC"

