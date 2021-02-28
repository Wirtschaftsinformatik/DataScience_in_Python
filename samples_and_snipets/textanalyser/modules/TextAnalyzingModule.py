from wordcloud import WordCloud
import matplotlib.pyplot as plt
from .TextProcessingModule import *
from collections import Counter
from spacy import displacy


class TextAnalyzing:

    def __init__(self, text):
        self.text = text
        self.processor = TextProcessing(text)
        self.removed_doc = self.processor.rmStopWords()
        self.doc = self.processor.get_doc()

    def wordcloud(self):

        # preprocessing
        stemmed_doc = self.processor.stemming(self.removed_doc)

        # generate word cloud
        wordcloud = WordCloud(
            background_color="white"
        ).generate(', '.join(stemmed_doc))

        # plot word cloud
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

    def top_keyword_freq_plt(self, n): # stopwords entfernen
        keywords = self.processor.keywords_extraction()


        keywords_stemmed = []

        for keyword in keywords:
            lem = self.processor.stemm_porter(keyword)
            keywords_stemmed.append(lem)

        print(keywords_stemmed)

        freq_words = self._word_freq(keywords_stemmed)

        top_ten = dict(freq_words.most_common(n))

        plt.bar(range(len(top_ten)), list(top_ten.values()), align='center')
        plt.xticks(range(len(top_ten)), list(top_ten.keys()), rotation=90)
        plt.show()

    # returns those sentences that includes the most frequent words
    def top_sentence(self, limit):
        keywords = self.processor.keywords_extraction()
        freq_words = self._word_freq(keywords)

        sent_strength = {}
        for sent in self.doc.sents:
            for word in sent:
                if word.text in freq_words.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent]+=freq_words[word.text]
                else:
                    sent_strength[sent] = freq_words[word.text]

        summary = []

        sorted_x = sorted(sent_strength.items(), key=lambda kv: kv[1], reverse=True)

        counter = 0

        for i in range(len(sorted_x)):
            summary.append(str(sorted_x[i][0]).capitalize())

            counter += 1

            if counter >= limit:
                break

        # strip linebreaks
        clean_summary = []
        for sentence in summary:
            clean_summary.append(sentence.replace("\n", ""))

        return "\n\n".join(clean_summary)

    def _word_freq(self, keywords):

        # count freq of words
        freq_words = Counter(keywords)
        max_freq = Counter(keywords).most_common(1)[0][1]
        # normalize freq
        for w in freq_words:
            freq_words[w] = (freq_words[w] / max_freq)

        return freq_words

    def get_entities(self, type): #ORG, CARDINAL, MONEY, PERSON, PERCENT, DATE, GPE, LANGUAGE
        for ent in self.doc.ents:
            if ( ent.label_ == type):
                print(ent.text, ent.start_char, ent.end_char, ent.label_)

    def display_entities(self):
        return displacy.render(self.doc, style="ent")









