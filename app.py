from flask import Flask, request, render_template, url_for, redirect
from flask.ext.pymongo import PyMongo
from flask_wtf import FlaskForm
from flaskrun import flaskrun
from wtforms import StringField, HiddenField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.login import LoginManager

app = Flask(__name__, static_url_path='')
app.secret_key = 'kittens'
app.config['MONGO_DBNAME'] = "test"
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class Citation(object):
    def __init__(self, mongoItem):
        for key in mongoItem:
            setattr(self, key, mongoItem[key])

class Meaning(object):
    def __init__(self, mongoItem):
        self.order = mongoItem["order"]
        self.definition = mongoItem["definition"]
        if "tags" in mongoItem:
            self.tags = mongoItem["tags"]
        if "cites" in mongoItem:
            self.citations = []
            for cite in mongoItem["cites"]:
                citation = Citation(cite)
                self.citations.append(citation)

class Lemma(object):
    def __init__(self, mongoItem):
        self.lemmaID = mongoItem["_id"]
        self.lemma = mongoItem["lemma"]
        self.pos = mongoItem["pos"]
        self.meanings = mongoItem["meanings"]
        self.type = mongoItem["type"]
        for meaning in self.meanings:
            meaningObject = Meaning(meaning)

class LemmaForEdit(object):
    def __init__(self, LemmaObject):
        self.lemmaID = LemmaObject.lemmaID
        self.lemma = LemmaObject.lemma
        for indx, meaning in enumerate(LemmaObject.meanings):
            name = "definition_" + str(indx)
            setattr(self, name, meaning["definition"])





@app.route('/')
def home_page():
    wordlist = mongo.db.dictionary.find({"$or": [{"type": "lemma"},{"type":"idiom"}]}, {"lemma":1, "pos":1}).sort("lemma", 1)
    return render_template('list.html',
        wordlist=wordlist, total=wordlist.count(), pagetitle="Home")

@app.route('/w/<word>')
def word(word):
    word = Lemma(mongo.db.dictionary.find_one_or_404({'_id': word}))
    return render_template('lemma.html', word=word, pagetitle=word.lemma)

@app.route('/e/<lemma_id>',methods=['GET','POST'])
def edit(lemma_id):
    return lemma_id

@app.route('/t/<tag>')
def tag(tag):
    wordlist = mongo.db.dictionary.find({"meanings.tags":tag}, {"lemma":1, "pos":1}).sort("lemma", 1)
    return render_template('list.html', wordlist=wordlist, total=wordlist.count(), pagetitle="[{}]".format(tag))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    flaskrun(app)
