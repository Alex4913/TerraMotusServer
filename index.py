#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from src import server

def main():
  mapDir = "maps"
  imageDir = "images"

  if(not(os.path.exists(mapDir)): os.mkdir(mapDir)
  if(not(os.path.exists(imageDir)): os.mkdir(imageDir)

  WSGIServer(server.WebServer(mapDir, imageDir).app).run()

if(__name__ == "__main__"): main()
