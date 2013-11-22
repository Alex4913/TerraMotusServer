#!/usr/bin/python
import cgi
import os

from src import imager

class WebServer(object):
  # Possible POST options
  uploadTag = "upload"
  fileNameTag = "filename"
  downloadTag = "download"
  listTag = "list"

  validResponse = "VALID"
  invalidResponse = "INVALID"

  # Simple method to both print and append to a log file (with timestamp)
  def log(self, message):
    f = open(Server.logFile, "a+")
    output = time.strftime("[%x, %X]") + ": " + message
    f.write(output + "\n")
    f.close()

  def __init__(self, mapDir = "", imageDir = "", headerPath = "header.html",
                 footerPath = "footer.html"):
    self.mapDir = mapDir
    self.imageDir = imageDir
    self.headerPath = headerPath
    self.footerPath = footerPath

    self.imgr = imager.Imager(self.mapDir, self.imageDir)

  def read(self, path):
    # Read a file in and return a string of it's contents
    f = open(path, "r")
    lines = ""
    for line in f:
      lines += line
  
    return lines
  
  def createMap(self, upload, filename):
    # Copy an input file to the mapDir

    # Add a number to the end of the file if one exists already
    # to avoid over-writing
    name = filename.value
    count = 1
    while(os.path.exists(name)):
      name = stripExtension(name) + str(count) + ".csv"

    # Catch errors with the directory structure, and return a
    # valid response if it works
    try:
      save = open(self.mapDir + "/" + name, "w+")

      f = upload.file
      for line in f:
        save.write(line)
      save.close()
      return WebServer.validResponse
    except:
      return WebServer.invalidResponse

  def downloadMap(self, filename):
    # Sendf a map to a client, filename and then contents
    send = open(self.mapDir + "/" + filename.value, "r")

    result = ""
    for line in send:
      result += line
    send.close()

    return filename.value + "\n" + result

  def listMaps(self, arg):
    # List availiable maps and interpret what the user wants
    val = arg.value
    maps = os.listdir(self.mapDir)
    if(val == "sorted"):
      maps = sorted(maps)

    if(len(maps) == 0):
      return ""
    else:
      result = maps[0]
      for name in xrange(1, len(maps)):
        result += ", " + name
      return result
      
  def noEntries(self):
    # If there are no maps
    s = ""
    s +=  "  <div class='content'>\n"
    s +=  "    <table class='content-table'>\n"
    s +=  "      <tr>\n"
    s +=  "        <td style='text-align:left'>No more maps?</td>\n"
    s +=  "      </tr>\n"
    s +=  "    </table>\n"
    s +=  "  </div>\n"
    return s
  
  def stripExtension(self, path):
    # Get rid of .xxx
    return path[:len(path) - 4]
  
  def imageToMap(self, path):
    # Get rid of .png
    path = stripExtension(path)
    return self.mapDir + "/" + path + ".csv"
  
  def entry(self, path):
    # HTML for each entry
    s = ""
    s +=  "  <div class='content'>\n"
    s +=  "    <table class='content-table'>\n"
    s +=  "      <tr>\n"
    s +=  ("        <td style='text-align:left'>" + self.stripExtension(path) + 
             "</td>\n")
    s +=  "        <td style='text-align:right'>\n"
    s +=  "          <form action='" + self.imageToMap(path) + "'>\n"
    s +=  ("            <input class='content-button' type='submit'" + 
             " value='Download'>\n")
    s +=  "          </form>\n"
    s +=  "        </td>\n"
    s +=  "      </tr>\n"
    s +=  "    </table>\n"
    s +=  "    <div class='content-map-image'>\n"
    s +=  ("      <img class='map-image' src='" + self.imageDir + "/" + path +
             "'>\n")
    s +=  "    </div>\n"
    s +=  " </div>\n"
    return s
  
  def dynamic(self):
    # Create an enry for each map
    files = os.listdir(self.imageDir)
    if(len(files) == 0):
      return self.noEntries()
    else:
      result = ""
      for f in files:
        result += self.entry(f)
      return result

  def buildPage(self):
    # Combine each part of the webpage
    return (self.read(self.headerPath) + self.dynamic() +
             self.read(self.footerPath))

  def app(self, environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/html")]
    page = None

    # Handle passed data
    form = cgi.FieldStorage(fp = environ["wsgi.input"], environ = environ)
    if(WebServer.uploadTag in form and WebServer.fileNameTag in form):
      headers = [("Content-type", "text/plain")]
      page = self.createMap(form[WebServer.uploadTag], 
                            form[WebServer.fileNameTag])
    elif(WebServer.downloadTag in form):
      headers = [("Content-type", "text/plain")]
      page = self.downloadMap(form[WebServer.downloadTag])
    elif(WebServer.listTag in form):
      headers = [("Content-type", "text/plain")]
      page = self.listMaps(form[WebServer.listTag])

    # If nothing was passed that needs to modify the page, go with the regular
    if(page is None): page = self.buildPage()
    self.imgr.update()
    
    start_response(status, headers)
    return page
