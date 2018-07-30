# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'minorproject.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from PyQt4 import QtCore, QtGui
import sys

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

symptoms = pd.read_csv('final_dataset/symptoms.csv')
sym_dia = pd.read_csv('final_dataset/sym_dia_final.csv')
diagonistics = pd.read_csv('final_dataset/diagonistics.csv')
medicine = pd.read_csv('final_dataset/med_1_2_3_4.csv')
symptoms_pre = symptoms.set_index("sid")
diagonistics_pre = diagonistics.set_index('did')
medicine_pre = medicine.set_index('did')
final_sym = []
final_list_case = []

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.symtom_list()
		self.setupUi(self)
    
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(804, 684)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.frame = QtGui.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(0, 10, 791, 641))
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.pushButton = QtGui.QPushButton(self.frame)
		self.pushButton.setGeometry(QtCore.QRect(510, 40, 99, 27))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.runningFn)
		self.plainTextEdit = QtGui.QPlainTextEdit(self.frame)
		self.plainTextEdit.setGeometry(QtCore.QRect(150, 120, 461, 181))
		self.plainTextEdit.setPlainText(_fromUtf8(""))
		self.plainTextEdit.setReadOnly(True)
		self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
		self.pushButton_2 = QtGui.QPushButton(self.frame)
		self.pushButton_2.setGeometry(QtCore.QRect(510, 320, 99, 27))
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.clicked.connect(self.prepare_the_output)
		self.plainTextEdit_2 = QtGui.QPlainTextEdit(self.frame)
		self.plainTextEdit_2.setGeometry(QtCore.QRect(150, 380, 471, 241))
		self.plainTextEdit_2.setObjectName(_fromUtf8("plainTextEdit_2"))
		self.plainTextEdit_2.setReadOnly(True)
		self.lineEdit = QtGui.QLineEdit(self.frame)
		self.lineEdit.setGeometry(QtCore.QRect(150, 20, 281, 71))
		self.lineEdit.setText(_fromUtf8(""))
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.lineEdit.setPlaceholderText("Enter Symptoms");
		self.lineEdit_2 = QtGui.QLineEdit(self.frame)
		self.lineEdit_2.setGeometry(QtCore.QRect(150, 320, 271, 27))
		self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
		self.lineEdit_2.setPlaceholderText("Enter Symptom Number");
		self.label = QtGui.QLabel(self.frame)
		self.label.setGeometry(QtCore.QRect(160, 360, 68, 17))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.frame)
		self.label_2.setGeometry(QtCore.QRect(160, 100, 68, 17))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 25))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.pushButton.setText(_translate("MainWindow", "Suggest", None))
		self.pushButton_2.setText(_translate("MainWindow", "Recommend", None))
		self.label.setText(_translate("MainWindow", "RESULT", None))
		self.label_2.setText(_translate("MainWindow", "SUGGEST", None))

	def prepare_the_output(self): 
		try:
			inp = int(str(self.lineEdit_2.text()))
			sid = final_list_case[inp-1][1]
			result_dataset = pd.DataFrame(columns = ['did','wei','diagnosis','medicine','life_threatening'])
			did = []
			wei = []
			diagonosis = []
			medicine = []
			life_threatening = []	
			for index, row in sym_dia.iterrows():
				if(row['sid'] == sid):
					did_i = row['did']
					dia_list = [] 
					did.append(did_i)
					wei.append(row['wei'])
					word_tokens = word_tokenize(str(diagonistics_pre.loc[did_i,"diagnosis"]))
					str1 = ''.join(word_tokens)	
					diagonosis.append(str1)	
					medicine.append(str(medicine_pre.loc[did_i,"medicine"]))
					if(int(symptoms_pre.loc[sid,"life_threatening"]) == 1):
						life_threatening.append("yes")
					else:
						life_threatening.append("no")
			max_wei = max(wei)
			result_dataset['did'] = did
			result_dataset['wei'] = wei
			result_dataset['diagonosis'] = diagonosis
			result_dataset['medicine'] = medicine	
			result_dataset['life_threatening'] = life_threatening
			
			result_dataset = result_dataset[result_dataset.wei == max_wei]
			result_dataset = result_dataset[['diagonosis','medicine','life_threatening']]
			#print(result_dataset.head(len(result_dataset.index)))
			final_output = ""		
			for i in range(len(result_dataset.index)):
				if(i==2):
					break
				final_output = final_output + "(D) " + result_dataset.iloc[i,0] + "   (M) " +result_dataset.iloc[i,1] + "   (L) " + result_dataset.iloc[i,2] + "\n" 	
		except:
			final_output = "\n No specific Treatment found.\nWe recommend you to change your Eating habits.\nDo some exercise daily.\nThank you"
		#print(final_output)
		flag = 0
		for i in range(len(final_list_case)):
			if(inp == final_list_case[i][0]):
				flag = 1
		if(flag == 0):
			final_output = "\n Wrong Option selected"
		self.plainTextEdit_2.clear()
		self.plainTextEdit_2.setPlainText(final_output)

	def symtom_list(self):
		for index, row in symptoms.iterrows():
			s = str(row['symptom'])
			s = s.lower()
			word_tokens = word_tokenize(s)
			filtered_sentence = [w for w in word_tokens if not w in stop_words]
			filtered_input = []
			filtered_input.append(str(row['sid']))
			for w in filtered_sentence:
				word = lemmatizer.lemmatize(w)
				word = ps.stem(w)	
				filtered_input.append(word)
			final_sym.append(filtered_input)
	
	# Our Main Function to find the Symptom 
	def runningFn(self):
		
		counter = 1
		sid_now = 0
		del final_list_case[:]
		#inp = input("Whats your Symptoms? \n")
		inp = str(self.lineEdit.text())
		inp = inp.lower()
		#print(inp)
		if(inp == "quit"):
			return

		word_tokens = word_tokenize(inp)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		filtered_input = []
		for w in filtered_sentence:
			word = lemmatizer.lemmatize(w)
			word = ps.stem(w)	
			filtered_input.append(word)
		
		list_case = []
		#final_list_case = []
		min_not_matched = 100
		min_sid = 0
		for l in final_sym:
			x = len(list(set(filtered_input) & set(l)))
			if(x == len(filtered_input) and x == (len(l))-1):
				list_case = [counter,int(l[0])]
				final_list_case.append(list_case)
				counter += 1
				break
			elif(x == len(filtered_input)):
				list_case = [counter,int(l[0])]
				final_list_case.append(list_case)
				counter += 1
			elif(x == (len(l))-1):
				list_case = [counter,int(l[0])]
				final_list_case.append(list_case)
				counter += 1
			elif((len(filtered_input) - x) < min_not_matched): 
				min_not_matched = (len(filtered_input) - x)
		
		final_sid = 0
		sym_select = ""
		if(len(final_list_case) > 0):
			sym_select = sym_select + "Select your Symptom by typing the number : "		
			for l in final_list_case:
				sym_select = sym_select + '\n' + str(l[0])  + ". " + str(symptoms_pre.loc[l[1],"symptom"])
			sym_select = sym_select + "\n\nType the number : "		
		else:
			sym_select = "No appropriate symptom found"
		#print(sym_select, end = '')
		self.plainTextEdit.clear()
		#self.plainTextEdit.setPlainText(_fromUtf8(""))
		self.plainTextEdit.setPlainText(sym_select)
		#inp = int(str(lineEdit_2.text()))
		#if(inp == 99):
		#	exit()
		#final_sid = final_list_case[inp-1][1]	
		#self.prepare_the_output(final_sid)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	#MainWindow = QMainWindow()
	ui = Ui_MainWindow()
	#ui.setupUi(MainWindow)
	ui.show()
	 
	sys.exit(app.exec_())
