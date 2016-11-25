import json
import xmltodict
import mwparserfromhell

def xmlToDict(filename):
    with open(filename, "r") as fd:
        doc=xmltodict.parse(fd.read())
    return doc

def saveDictAsJsonFile(doc, filename):
    with open(filename, "w") as fp:
        fp.write(json.dumps(doc, indent=4, sort_keys=False))

def printMainspaceTitles(doc):
    for page in doc["mediawiki"]["page"]:
        if page["ns"] == "0":
            print(page["title"])

def getTextByTitle(doc, pagetitle):
    for page in doc["mediawiki"]["page"]:
        if page["title"] == pagetitle:
            return page["revision"]["text"]["#text"]

def getSectionInLanguage(article, language):
    parsed = mwparserfromhell.parse(article)
    return parsed.get_sections(levels=[2], matches=language)

def getArticlesInLanguage(doc, language):
    articles = []
    for page in doc["mediawiki"]["page"]:
        if page["ns"] == "0":
            parsed = getSectionInLanguage(page["revision"]["text"]["#text"], language)
            if len(parsed) > 0:
                articles.append(parsed)
    return articles

if __name__ == "__main__":
    doc = xmlToDict("small.xml")
    swedishArticles = getArticlesInLanguage(doc, "Svenska")
    print(swedishArticles[0][0])
