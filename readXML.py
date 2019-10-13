import xmltodict
import json
import os

dir = './../../NGSCWork/VivaGraphJS/demos/tutorial_svg/gexfFolder/'

for fName in os.listdir(dir):
    doc = {}
    with open(dir+fName) as fd:
        doc = xmltodict.parse(fd.read())
        fd.close()

    jsonOb = json.dumps(doc)
    with open('NGSCOutput/'+fName+'.json','w') as fOut:
        fOut.write(jsonOb)
        fOut.close()
