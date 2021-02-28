# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from model import Model
from modules.TextExtractorModule import File
from strings import debug_strings, warning_string, info_string
from datetime import datetime


class MainWindowUIClass(QtWidgets.QMainWindow):
    def __init__(self):
        """Initialize the super class AND define slots here!!!"""
        super().__init__()
        self.ui = uic.loadUi("mainTextanalyser.ui", self)

        # add model to hold values
        self.model = Model()

        # add here all custom slots and ui widgets
        self.pushButton_browse.clicked.connect(self.browseDirectory)
        self.pushButton_quit.clicked.connect(self.quit)
        self.pushButton_loadData_2.clicked.connect(self.process_pdf)
        self.pushButton_wordCloud.clicked.connect(self.display_wordcloud)
        self.pushButton_topkeyword.clicked.connect(self.display_top_keyword)
        self.pushButton_topSentence.clicked.connect(self.display_top_sentences)
        self.pushButton_entities.clicked.connect(self.display_entities)
        self.pushButton_exportResults.clicked.connect(self.display_wordcloud)
        self.comboBox.addItems(["english"])

        # reset progressbar to zero
        self.progressBar_2.setValue(0)

    def display_wordcloud(self):
        self.debugPrint(debug_strings["debug_wordcloud"])
        if self.info_dialog(self.model.getAnalyzedText(), warning_string["text_not_analyzed_msg"], warning_string["text_not_analyzed"]):
            return
        analyzedText = self.model.getAnalyzedText()
        analyzedText.wordcloud()

    def display_entities(self):
        self.debugPrint(debug_strings["debug_entities"])
        if self.info_dialog(self.model.getAnalyzedText(), warning_string["text_not_analyzed_msg"], warning_string["text_not_analyzed"]):
            return
        analyzedText = self.model.getAnalyzedText()
        html = analyzedText.display_entities()
        self.textBrowser_log.clear()
        self.textBrowser_log.setHtml(html)

    def display_top_sentences(self):
        self.debugPrint(debug_strings["debug_top_sentence"])
        if self.info_dialog(self.model.getAnalyzedText(), warning_string["text_not_analyzed_msg"], warning_string["text_not_analyzed"]):
            return
        analyedText = self.model.getAnalyzedText()
        top_sentence = analyedText.top_sentence(3)
        self.resultMsgBoxPrint(top_sentence)


    def display_top_keyword(self):
        self.debugPrint(debug_strings["debug_top_keyword"])
        if self.info_dialog(self.model.getAnalyzedText(), warning_string["text_not_analyzed_msg"], warning_string["text_not_analyzed"]):
            return
        analyzedText = self.model.getAnalyzedText()
        analyzedText.top_keyword_freq_plt(10)

    def process_pdf(self):
        self.debugPrint(debug_strings["debug_extract_text"])
        # handle fileNotProvided
        if self.info_dialog(self.model.fileName, warning_string["file_not_found"], warning_string["missing_path_or_filename"]):
            return
        # diable the mainwindow until text is loaded
        MainWindow.setEnabled(False)

        self.debugPrint(info_string["loading_text"])
        file = File()
        text = file.extract_text(self.model.getFileName(), self.progressBar_2)
        self.model.setText(text)
        self.debugPrint(info_string["load_text_successfully"])

        # enable the mainwindow afterwards
        MainWindow.setEnabled(True)

    def info_dialog(self, verify_obj, msg, debug_msg):
        if verify_obj is None:
            self.debugPrint(debug_msg)
            msgDialog = QtWidgets.QMessageBox()
            msgDialog.setText(msg)
            msgDialog.setIcon(QtWidgets.QMessageBox.Warning)
            msgDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgDialog.exec_()
            return True


    def readParameter(self):
        """ reads the parameter file in one dictionary :return: dictionary"""
        import json
        with open('parameter.json', 'r', encoding='utf-8') as f:
            parameter = json.load(f)
        return parameter

    # setup
    def setupUi(self, mainWindow):
        """ do all initial of current window here"""
        self.tabWidget.setCurrentIndex(0)
        self.version.setText(str(parameter['app']['version']))
        self.releaseDate.setText(str(parameter['app']['release_date']))
        self.license.setText(str(parameter['app']['license']))

    # print results
    def resultMsgBoxPrint(self, msg):
        self.textBrowser_log.clear()
        timestamp = datetime.now()
        self.textBrowser_log.append("Log  " + timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.textBrowser_log.append(msg)

    # debugging
    def debugPrint(self, msg=debug_strings["debug_default"]):
        timestamp = datetime.now()
        self.textBrowser_debug.append("Log Debug " + timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.textBrowser_debug.append(msg)

    # refresh UI
    def refreshAll(self):
        self.lineEdit.setText(self.model.getFileName())

    # 'custom' slot
    # no 'custom' slots implemented directly in QT because of class overloading issues
    def browseDirectory(self):
        """ Called when the user presses the Browse button"""
        self.debugPrint(debug_strings["debug_browse"])
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Please select file", "",
                                                            "*.pdf", options=options)
        if fileName:
            self.debugPrint(info_string["set_filename"] + fileName)
            self.model.setFileName(fileName)
            self.refreshAll()

    # exit
    def quit(self):
        sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    parameter = ui.readParameter()
    ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())
