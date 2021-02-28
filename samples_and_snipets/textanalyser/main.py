from modules.TextExtractorModule import File
from modules.TextProcessingModule import *
from modules.TextAnalyzingModule import *


def main():

    # load pdf
    file = File()
    text = file.extract_text('test.pdf')

    # analyze text
    analyze = TextAnalyzing(text)
    #analyze.wordcloud()
    analyze.top_keyword_freq_plt(20)
    #print(analyze.top_sentence(3))
    analyze.get_entities('PERSON')
    analyze.display_entities()


if __name__ == "__main__":
    main()
