from modules.TextAnalyzingModule import TextAnalyzing

class Model:
    def __init__(self):
        self.fileName = None
        self.text = None
        self.analyzedText = None

    @staticmethod
    def isValid(file_name):
        """ returns True if the file exists and can be opened.  Returns False otherwise."""
        try:
            file = open(file_name, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, file_name):
        """ sets member filename to the filename if it exists """
        if self.isValid(file_name):
            self.fileName = file_name
        else:
            self.fileName = ""

    def getFileName(self):
        """ returns the name of the file name member. """
        return self.fileName

    def setText(self, text):
        """ sets member text to extracted text an creates the analyze instance"""
        self.text = text
        self.analyzedText = TextAnalyzing(self.text)

    def getText(self):
        """ returns the extracted Text"""
        return self.text

    def getAnalyzedText(self):
        return self.analyzedText


