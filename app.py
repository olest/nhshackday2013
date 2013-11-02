
import os
import logging
import time

FORMAT='[%(levelname)s] (%(pathname)s %(asctime)s): %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import bottle
from bottle import Bottle, redirect, request, abort, response, static_file

import pystache

import config

app = Bottle()


@app.route('/')
def index():
    return static_file("index.html", root=config.STATIC_PATH) 




@app.route("/<filepath:path>")
def serve_static(filepath):
  if os.access(os.path.join(config.STATIC_PATH, filepath), os.R_OK):
    # I can read the file OK
    return static_file(filepath,root=config.STATIC_PATH)
  else:
    abort(404, "Could not find resource specified")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=config.PORT, reloader=config.DEVELOPMENT)
