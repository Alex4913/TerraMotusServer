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
    f = open(path, "r")
    lines = ""
    for line in f:
      lines += line
  
    return lines
  
  def createMap(self, upload, filename):
    save = open(self.mapDir + "/" + filename.value, "w+")

    f = upload.file
    for line in f:
      save.write(line)
    save.close()

  def downloadMap(self, filename):
    send = open(self.mapDir + "/" + filename.value, "r")

    result = ""
    for line in send:
      result += line
    send.close()

    return filename.value + "\n" + result

  def listMaps(self, arg):
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
    s = ""
    s +=  "  <div class='content'>\n"
    s +=  "    <table class='content-table'>\n"
    s +=  "      <tr>\n"
    s +=  "        <td style='text-align:left'>No more maps?</td>\n"
    s +=  "      </tr>\n"
    s +=  "    </table>\n"
    s +=  "  </div>\n"
    return s
  
  def imageToMap(self, path):
    # Get rid of .png
    path = path[:len(path) - 4]
    return self.mapDir + "/" + path + ".csv"
  
  def imageToName(self, path):
    # Get rid of .csv
    return path[:len(path) - 4]
  
  def entry(self, path):
    s = ""
    s +=  "  <div class='content'>\n"
    s +=  "    <table class='content-table'>\n"
    s +=  "      <tr>\n"
    s +=  "        <td style='text-align:left'>" + self.imageToName(path) + "</td>\n"
    s +=  "        <td style='text-align:right'>\n"
    s +=  "          <form action='" + self.imageToMap(path) + "'>\n"
    s +=  "            <input class='content-button' type='submit' value='Download'>\n"
    s +=  "          </form>\n"
    s +=  "        </td>\n"
    s +=  "      </tr>\n"
    s +=  "    </table>\n"
    s +=  "    <div class='content-map-image'>\n"
    s +=  "      <img class='map-image' src='" + self.imageDir + "/" + path + "'>\n"
    s +=  "    </div>\n"
    s +=  " </div>\n"
    return s
  
  def dynamic(self):
    files = os.listdir(self.imageDir)
    if(len(files) == 0):
      return self.noEntries()
    else:
      result = ""
      for f in files:
        result += self.entry(f)
      return result

  def buildPage(self):
    return self.read(self.headerPath) + self.dynamic() + self.read(self.footerPath)

  def app(self, environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/html")]
    page = None

    form = cgi.FieldStorage(fp = environ["wsgi.input"], environ = environ)
    if(WebServer.uploadTag in form and WebServer.fileNameTag in form):
      self.createMap(form[WebServer.uploadTag], form[WebServer.fileNameTag])
    elif(WebServer.downloadTag in form):
      headers = [("Content-type", "text/plain")]
      page = self.downloadMap(form[WebServer.downloadTag])
    elif(WebServer.listTag in form):
      headers = [("Content-type", "text/plain")]
      page = self.listMaps(form[WebServer.listTag])

    if(page is None): page = self.buildPage()
    self.imgr.update()
    
    start_response(status, headers)
    return page
