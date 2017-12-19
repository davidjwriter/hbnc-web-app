#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskr/")

from flaskr import app as application
application.secret_key = 'lht+)8on!@s)dw!ikizr=59h=4f8x=vziupnpnv-h=8fh)ki*g'
