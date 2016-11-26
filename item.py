class Citation(EmbeddedDocument()):
	author = StringField(required=True)
	content = StringField(required=True)
	date = DateTimeField(required=True)
	tags = ListField(StringField(), required=False)
	url = URLField(required=False)
	work = StringField(required=False)

class Meaning(EmbeddedDocument()):
	cites = ListField(Citation(), required=False)
	definition = StringField(required=True)
	examples = ListField(StringField(), required=False)
	order = IntField(required=True)

class DictItem(Document):
	item_id = StringField(required=True)

class Lemma(DictItem):
	tags = ListField(StringField(), required=False)
	pos = StringField(required=True)
