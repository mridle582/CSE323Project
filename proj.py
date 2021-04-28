#! /usr/bin/python
import sys
from FrontEnd.modules import FrontEnd


if __name__ == '__main__':
    fe = FrontEnd()
    fe.set_gui()
    sys.exit(fe.run_gui())
