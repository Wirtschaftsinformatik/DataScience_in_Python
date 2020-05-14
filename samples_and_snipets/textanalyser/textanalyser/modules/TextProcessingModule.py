import spacy


class TextProcessing:

    def __init__(self, text, language='en'):
        self.text = text
        self.language = language

        # initialize spaCy model for specific language
        # add new languages here
        if language == "en":
            self.nlp = spacy.load(self.language)
        self.doc = self.nlp(self.text)

    def __tokenize(self):

        return [token.text for token in self.doc]

