# importing the libraries
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# loading the datasets
symptoms = pd.read_csv('final_dataset/symptoms.csv')
sym_dia = pd.read_csv('final_dataset/sym_dia_final.csv')
diagonistics = pd.read_csv('final_dataset/diagonistics.csv')
medicine = pd.read_csv('final_dataset/med_1_2_3_4.csv')
symptoms_pre = symptoms.set_index("sid")
diagonistics_pre = diagonistics.set_index('did')
medicine_pre = medicine.set_index('did')
final_sym = []

# Prepare the output for printing
def prepare_the_output(sid): 
	try:
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
			final_output = final_output + "(D) " + result_dataset.iloc[i,0] + " (M) " +result_dataset.iloc[i,1] + " (L) " + result_dataset.iloc[i,2] + "\n" 	
	except:
		final_output = "\n No specific Treatment found.\nWe reccomend you to change your Eating habits.\nDo some exercise daily.\nThank you"
	print(final_output)
# Apply NLP to the symptoms dataset to compare the sets easily
def symtom_list():
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
	#print(final_sym[0])
	#print(final_sym[474])

# Our Main Function to find the Symptom 
def runningFn():
	
	counter = 1
	sid_now = 0
	inp = input("Whats your Symptoms? \n")
	inp = inp.lower()
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
	final_list_case = []
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
	'''if(min_not_matched > 0 and min_not_matched is not 100):
		for l in final_sym:
			x = len(list(set(filtered_input) & set(l)))
			if((len(filtered_input) - x) == min_not_matched):
				list_case = [counter,int(l[0])]
				final_list_case.append(list_case)
				counter += 1
	'''
	final_sid = 0
	sym_select = ""
	if(len(final_list_case) > 0):
		sym_select = sym_select + "Select your Symptom by typing the number : "		
		for l in final_list_case:
			sym_select = sym_select + '\n' + str(l[0])  + ". " + str(symptoms_pre.loc[l[1],"symptom"])
		sym_select = sym_select + "\nType the number : "		
	else:
		sym_select = "No appropriate symptom found\ntype 99 to exit : "
	print(sym_select, end = '')
	inp = int(input())
	if(inp == 99):
		exit()
	final_sid = final_list_case[inp-1][1]	
	prepare_the_output(final_sid)


symtom_list()
runningFn()
