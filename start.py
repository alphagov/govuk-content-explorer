#!/usr/bin/env python

import explorer
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        debug = True
    else:
        debug = False
    explorer.app.run(debug=debug)
