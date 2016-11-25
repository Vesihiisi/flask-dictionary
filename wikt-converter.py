import json
import xmltodict
import re
import mwparserfromhell

def printNice(doc):
    print(json.dumps(doc, indent=4, sort_keys=False))

def xmlToDict(filename):
    with open(filename, "r") as fd:
        doc=xmltodict.parse(fd.read())
    return doc

def saveDictAsJsonFile(doc, filename):
    with open(filename, "w") as fp:
        fp.write(json.dumps(doc, indent=4, sort_keys=True, ensure_ascii=False))

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
    articles = {}
    for page in doc["mediawiki"]["page"]:
        if page["ns"] == "0":
            parsed = getSectionInLanguage(page["revision"]["text"]["#text"], language)
            if len(parsed) > 0:
                pagetitle = page["title"]
                articles[pagetitle] = parsed[0]
    return articles

def getPosSections(article):
    sectionList = {}
    parsed = mwparserfromhell.parse(article).get_sections(levels=[3])
    for section in parsed:
        pos = section.split('\n', 1)[0]
        pos = re.sub('^[^a-zA-z]*|[^a-zA-Z]*$','', pos)
        sectionList[pos] = section
    return sectionList

if __name__ == "__main__":
    doc = xmlToDict("small.xml")
    swedishArticles = getArticlesInLanguage(doc, "Svenska")
    wordlist = []
    for art in swedishArticles:
        example = swedishArticles[art]
        sections = getPosSections(example)
        for s in sections:
            article = {}
            article["lemma"] = art
            article["pos"] = s
            article["meanings"] = []
            text = sections[s]
            remainder = []
            allLines = text.split("\n")
            for indx, line in enumerate(allLines):
                if len(line) > 0 and line[0] == "#" and line[1] != ":":
                    meaning = {}
                    templates = mwparserfromhell.parse(line).filter_templates()
                    if len(templates) > 0 and templates[0].name == "böjning":
                        definition = "böjningsform"
                    else:
                        definition = mwparserfromhell.parse(line).strip_code().strip()
                    number = len(article["meanings"]) + 1
                    meaning["order"] = number
                    meaning["definition"] = definition
                    meaning["remainder"] = []
                    meaning["examples"] = []
                    article["meanings"].append(meaning)
                    try:
                        nextLine = allLines[indx+1]
                        increaseIndex = 1
                        while len(nextLine) > 0 and nextLine[0] == "#" and nextLine[1] == ":":
                            lineContent = nextLine[2:]
                            parsedLineContent = mwparserfromhell.parse(lineContent)
                            if len(mwparserfromhell.parse(lineContent).filter_templates()) == 0: # no templates means it's an example sentence
                                exampleSentence = parsedLineContent.strip_code()
                                meaning["examples"].append(exampleSentence)
                            else:
                                meaning["remainder"].append(lineContent)
                            increaseIndex = increaseIndex + 1
                            nextLine = allLines[indx + increaseIndex]
                    except IndexError:
                        pass
            print("processed: {} ({})".format(art, s))
            wordlist.append(article)
        saveDictAsJsonFile(wordlist, "test_results.json")
