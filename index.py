#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
import os, stat

from src import server

def createDir(path):
  # Create a directory with the right permissions
  os.mkdir(path)

  # Read, write, execute by User, Group, Others
  os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

def main():
  mapDir = "maps"
  imageDir = "images"

  # Make the directories if they don't exist with highest permissions
  if(not(os.path.exists(mapDir))): createDir(mapDir)
  if(not(os.path.exists(imageDir))): createDir(imageDir)

  # Start the app
  WSGIServer(server.WebServer(mapDir, imageDir).app).run()

# Run main
if(__name__ == "__main__"): main()
