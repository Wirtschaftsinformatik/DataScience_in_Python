# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MainWindowUIClass(QtWidgets.QMainWindow):
	def __init__( self ):
		'''Initialize the super class
		AND define slots here!!!
		'''
		super().__init__()
		self.ui = uic.loadUi("mainForm.ui", self)

		# add here all custom slots...
		self.pushButton_getDirectoryName.clicked.connect(self.getDirectoryName)
		self.pushButton_getFileName.clicked.connect(self.getFileName)
		self.pushButton_quit.clicked.connect(self.quit)

	def readParameter(self):
		'''
		reads the parameter file in one dictionary
		:return:
		dictioanry
		'''
		import json
		with open('parameter.json', 'r', encoding='utf-8') as f:
			parameter = json.load(f)
		return parameter

	def setupUi( self, mainWindow ):
		''' do all initial of current window here
		'''
		self.tabWidget.setCurrentIndex(0)
		self.version.setText(str(parameter['app']['version']))
		self.releaseDate.setText(str(parameter['app']['release_date']))
		self.license.setText(str(parameter['app']['license']))

	def debugPrint( self, *, msg='no debug message provided'):
		self.textBrowser_debug.append(msg)

	# 'custom' slot
	# no 'custom' slots implemented directly in QT because of class overloading issues
	def getDirectoryName( self ):
		''' Called when the user presses the Browse button
		'''
		self.debugPrint( msg="getDirectoryName button pressed" )
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		dirName = QtWidgets.QFileDialog.getExistingDirectory(None, caption= "Please select directory")
		if dirName:
			self.debugPrint( msg = "setting dir name: {}".format(dirName))
		self.dirName.setText(dirName)

	def getFileName( self ):
		self.debugPrint( msg="getFileName button pressed" )
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Please select file", "", "All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			self.debugPrint( msg = "setting file name: " + fileName )
		self.fileName.setText(fileName)

	def quit(self):
		sys.exit(app.exec_())

if __name__ =='__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = MainWindowUIClass()
	parameter = ui.readParameter()
	ui.setupUi(MainWindow)
	ui.show()
	sys.exit(app.exec_())
