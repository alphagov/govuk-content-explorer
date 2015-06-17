#!/usr/bin/env python

from explorer import app
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        debug = True
    else:
        debug = False
    app.run(debug=debug, host='0.0.0.0')
