#!/usr/bin/python

import udeckHid, time

def main():
  udh = udeckHid.UdeckHid()
  time.sleep(20)
  udh.sendWindowKey('r')
  time.sleep(2)
  udh.sendLine('notepad')
  time.sleep(2)
  for i in range(0, 50):
    udh.sendString('You are so hacked\n')
  time.sleep(2)
  udh.sendAltKey('f')
  udh.sendChar('x')
  udh.sendEnter()
  time.sleep(2)
  udh.sendLine('hacked.txt')
  udh.sendWindowsUpsideDownScreen()
  udh.sendWindowsLockScreen()

if __name__ == "__main__":
  main()

