import json
import xmltodict

xmlFile = "small.xml"
with open("small.xml", "r") as fd:
    doc=xmltodict.parse(fd.read())

with open("result.json", "w") as fp:
    fp.write(json.dumps(doc, indent=4, sort_keys=False))

for page in doc["mediawiki"]["page"]:
    if page["ns"] == "0":
        print(page["title"])
