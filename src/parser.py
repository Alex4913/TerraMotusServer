import csv
import copy

def stringArrayToFloat(array):
  """ Convert a 2D list with string values to the same list with floats """
  returnArray = []
  for row in array:
    rowData = []
    for col in row:
      rowData += [float(col)]
    returnArray += [rowData]

  return returnArray

def parse(planeName):
  """ Open a data CSV and return a 2D list of floats """
  f = open(planeName, 'r')
  reader = csv.reader(f, delimiter=',')

  data = []
  for row in reader:
    data += [row]

  f.close()
  return (stringArrayToFloat(data), planeName)
