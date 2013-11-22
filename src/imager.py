import Image
import os
from src import parser

class Imager(object):
  def __init__(self, mapDir, imageDir):
    self.mapDir = mapDir
    self.imageDir = imageDir

  def getBounds(self, data):
    # Doing both simultaneously saves time
    minVal = None
    maxVal = None
    for row in data:
      minVal = min(minVal, min(row)) if(minVal is not None) else min(row)
      maxVal = max(maxVal, max(row)) if(maxVal is not None) else max(row)

    return (minVal, maxVal)

  def heightToColor(self, val, minVal, maxVal):
    # Needs to return a tuple, as PIL requires an immutable type in the image
    # Simple grayscale

    valScale = 255
    valRange = maxVal - minVal
    # Flat plane
    if(valRange == 0): return tuple([int(valScale/2)]*3)

    return tuple([int((float(val - minVal) / valRange) * valScale)] * 3)

  def generateImage(self, name):
    path = self.mapDir + "/" + name if(self.mapDir != "") else name

    # Get CSV data
    (data, _) = parser.parse(path + ".csv")
    (rows, cols) = (len(data), len(data[0]))
    (minVal, maxVal) = self.getBounds(data)

    # Construct color data
    colorData = []
    for row in xrange(rows):
      temp = []
      for col in xrange(cols):
        temp += [self.heightToColor(data[row][col], minVal, maxVal)]
      colorData += temp

    # Save image
    img = Image.new("RGB", (cols, rows))
    img.putdata(colorData)
    path = self.imageDir + "/" + name if(self.imageDir != "") else name
    img.save(path + ".png", "PNG")

  def update(self):
    for fileName in os.listdir(self.mapDir):
      # Get rid of csv extension
      name = fileName[:len(fileName) - 4]
      if(name + ".png" not in os.listdir(self.imageDir)):
        self.generateImage(name)
      
    for fileName in os.listdir(self.imageDir):
      # Get rid of png extension
      name = fileName[:len(fileName) - 4]
      if(name + ".csv" not in os.listdir(self.mapDir)):
        path = self.imageDir + "/" + name if(self.imageDir != "") else name
        os.remove(path + ".png")
