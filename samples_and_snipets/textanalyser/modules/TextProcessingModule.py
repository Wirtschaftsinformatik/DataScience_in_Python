import spacy
from string import punctuation
from spacy.lemmatizer import Lemmatizer
from nltk.stem import PorterStemmer

class TextProcessing:

    def __init__(self, text, language='en_core_web_sm'):
        self.text = text
        self.language = language

        # initialize spaCy model for specific language
        # add new languages here

        if language == "en_core_web_sm":
            self.nlp = spacy.load(self.language)
        self.doc = self.nlp(self.text.lower())

    def get_doc(self):
        return self.doc

    def __tokenize(self):

        return [token.text for token in self.doc]

    def __sentenize(self):
        sentences = list(self.doc.sents)

        return [sentence.text for sentence in sentences]

    def rmStopWords(self):

        filtered_sent = []

        for word in self.doc:
            if word.is_stop == False:
                filtered_sent.append(word)

        return filtered_sent

    @staticmethod
    def stemming(processed_doc):

        return [word.lemma_ for word in processed_doc]

    def stemm_porter(self, word):
        ps = PorterStemmer()

        return ps.stem(word)

    def keywords_extraction(self):
        keywords = []

        pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

        for token in self.doc:
            if (token.text in self.nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if (token.pos_ in pos_tag):
                keywords.append(token.text)

        return keywords


