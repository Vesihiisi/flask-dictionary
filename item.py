class Citation(EmbeddedDocument()):
	author = StringField(required=True)
	content = StringField(required=True)
	date = DateTimeField(required=True)
	url = URLField(required=False)
	work = StringField(required=False)

class DictItem(Document):
	lemma_id = StringField(required=True)

class Lemma(DictItem):
	tags = ListField(StringField(required=False))
