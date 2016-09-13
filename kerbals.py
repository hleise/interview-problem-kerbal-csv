from sys import argv
from csv import DictReader
from json import dumps
from xml.dom.minidom import parseString
from math import atan, pi

# Returns a given dataList as a kerbals XML DOM
def getKerbalsXML(dataList):
    dom = parseString("<kerbals></kerbals>")
    for object in dataList:
        objectNode = dom.createElement("kerbal")
        for key in object:
            keyNode = dom.createElement(key)
            keyNodeValue = dom.createTextNode(str(object[key]))
            keyNode.appendChild(keyNodeValue)
            objectNode.appendChild(keyNode)

        dom.childNodes[0].appendChild(objectNode)

    return dom

# Returns a dataList with all values in the given keysToConvert array converted into their "true values"
def convertToTrueValues(dataList, keysToConvert):
    for object in dataList:
        for key in object:
            if key in keysToConvert:
                object[key] = ((atan(object[key]) + (pi/2)) / (pi / 100)) # Calculates the true value
    return dataList

# Converts the appropriate values in the given dataList to either floats or integers.
def convertToNumbers(dataList):
    for object in dataList:
        for key in object:
            try:
                if '.' in object[key]:
                    object[key] = float(object[key])
                else:
                    object[key] = int(object[key])
            except ValueError: # Handles a ValueError if the value can't be converted to a float or integer.
                continue

    return dataList

if __name__ == "__main__":
    if len(argv) <= 2:
        csv = convertToNumbers(list(DictReader(open("kerbals.csv")))) # Reads the csv file to a list of dictionaries
        csv = convertToTrueValues(csv, ["Courage", "Stupidity"]) # Converts courage and stupidity to their "true values"
        if len(argv) == 1 or argv[1].lower() == "json":
            print(dumps(csv, indent = 4, sort_keys = True)) # Prints the csv data as json
        elif argv[1].lower() == "xml":
            print(getKerbalsXML(csv).toprettyxml()) # Prints the csv data as xml
        else:
            print("Invalid parameter. Enter either 'json' or 'xml'")
    else:
        print("Invalid parameters. Enter either 'json' or 'xml' with no additional parameters.")