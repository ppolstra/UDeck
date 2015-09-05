# UDeck
The UDeck or USB Deck is an addon to Deck Linux.
Deck Linux is a pentesting Linux which was created
for the BeagleBoard and BeagleBone family of devices
and also for similar devices.

The UDeck does not require that it be installed over
Deck Linux.  If you want to use the scriptable keyboard, 
you will need a 4.x kernel for this to work properly.

The scripts in the UDeck have the following functions:

mount-usb.sh: Exports a USB drive attached to the BBB
              as read-only to a PC which the BBB is
              plugged in to.

mount-usb-rw.sh: Makes a drive previously exported with
                 mount-usb.sh writeable.  

impersonator.sh: This will cycle through the VID/PID
                 combinations in vidpid-list until it
                 is killed.  This allows you to bypass
                 endpoint security software that filters
                 based on VID/PID.  If you know the 
                 appropriate VID/PID that should work
                 you can easily modify this script to
                 go directly to the appropriate VID/PID.

create-hid.sh: This creates a scriptable USB HID keyboard
               device on the BBB.  You could then send
               HID reports directly to this new device or
               you can use udeckHid.py to make this easy.

udeckHid.py: This is defines a set of Python classes that
             make scripting a HID keyboard much easier.
             There is also an example Linux script in this
             file.

attackWindows.py: This is an example of how the scriptable
                  HID keyboard can be used under Windows.
