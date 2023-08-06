import json
import sys
import re
import csv
import tarfile
import os
import shutil
import pickle
import nltk
import spacy
import pandas as pd
import wordninja
from nltk import tokenize
nltk.download('punkt')
spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")
from importlib import resources
import io



def clean_text(string):

	#Replace '..' with '.'	
	content= string.replace(r'..', '.')


	#Remove all of the spaces in the text.
	content=re.sub(r'\s+', '', content)

	#Replace decimal numbers(a.b as a[DOT]b)

	content = re.sub(r"(\d)\.(\d)", r"\1[DOT]\2", content) 

	#Replace the number that starts in the new line such as 1., 2. -> [item]

	content = re.sub(r'\d{1}\.','[item] ', content)

	#Replace bak [DOT] by '.'
	content=content.replace("[DOT]", ".")


	#The following code is to remove that sentence with 'results were'

	content = re.sub(r"\.\w*\W*\w*resultswere\w*.*$", "", content, flags=re.IGNORECASE)
	if content[-1]!='.':
		content+='.'

	#Word ninja -> This is used to segment the text we have earlier
	start=0
	string_tmp=''
	for i in range(len(content)):
	  if content[i]=='.':
	      lst=wordninja.split(content[start:i])
	      string_tmp+=' '.join(lst)
	      string_tmp+='.'
	      start=i+1
	      i=start


	string=string_tmp.replace("item","[item]")


	# replace dots that have numbers around them with "[DOT]"
	string1_protected = re.sub(r"(\d)\.(\d)", r"\1[DOT]\2", string)  
	# now split (and remove empty lines)
	lines_protected = [line + "." for line in string1_protected.split(".") if line]   
	# now re-replace all "[DOT]"s
	lines = [line.replace("[DOT]", ".") for line in lines_protected]



	#dict1 stores all the lines present in the above lines list
	dict1={}
	for index, string in enumerate(lines):
		dict1[index]=string

	#dict1 looks like below
	'''{0: '[item] Anatomical variant in the pulmonary venous structures on the right.',
 		1: '[item] Coronary calcification s and LC A variant as described.'}
 	'''

	#The following is used to verify and delete if the sentences are repeated multiple times.
	similarity_dict1={}
	for index1 in range(len(lines)):
		for index2 in range(index1+1,len(lines)):
	  		doc1 = nlp(lines[index1])
	  		doc2 = nlp(lines[index2])
	  		if doc1.similarity(doc2)>0.99 and index1!=index2:
	  			if index1 not in similarity_dict1:
	  				similarity_dict1[index1]=[]
	  			similarity_dict1[index1].append(index2)

	'''The similarity dict looks like below:
	{0:[1],2:[3]}
	line0 is similar to 1, and line 2 is similar to 3
	'''
	#if similarity dict is not empty then the list of lines for each key in the similarity dict are removed in dict1.

	if similarity_dict1:
		keys=list(dict1.keys())
		for index in keys:
			if index in similarity_dict1:
		  		for indexes in similarity_dict1[index]:
		  			del dict1[indexes]


	lst1=list(dict1.values())


	# read text file
	with resources.open_text('text_cleaning_velagala', 'vocab.txt') as fp:
	    text = BytesIO(fp.read())

	# Vocab file contains list of medical vocabulary
	# with open('vocab.txt', 'r') as f:    
	# 	text=f.read()

	'''
	As word ninja is already applied earlier, In the following blocks of code considering the tradeoff 
	5grams and 4grams and trigrams are applied on the each line in the dict in a sequential manner
	and if ngrams exists in medical vocabulary then it is replaced to make sure medical terms are merged correctly.
	'''
	from nltk import ngrams
	lst_after_5grams=[]
	lst_after_4grams=[]
	lst_after_trigrams=[]

	for sentence in lst1:
		pentagrams = ngrams(sentence.split(), 5)

		for grams in pentagrams:
		  exist=' '.join(grams)
		  check= ''.join(grams)
		  if check in text:
		    sentence= sentence.replace(exist,check)
		lst_after_5grams.append(sentence)

	for sentence in lst_after_5grams:
		tetragrams = ngrams(sentence.split(), 4)

		for grams in tetragrams:
		  exist=' '.join(grams)
		  check= ''.join(grams)
		  if check in text:
		    sentence= sentence.replace(exist,check)
		lst_after_4grams.append(sentence)

	for sentence in lst_after_4grams:
		trigrams = ngrams(sentence.split(), 3)

		for grams in trigrams:
		  exist=' '.join(grams)
		  check= ''.join(grams)
		  if check in text:
		    sentence= sentence.replace(exist,check)
		lst_after_trigrams.append(sentence)

	final_lst=[]
	for sentence in lst_after_trigrams:
		words=sentence.split()
		result = []
		for element in words :
			if len(result) == 0 or element != result[-1]:
				result.append(element)
		final_lst.append(' '.join(result))


	final_str=' '.join(final_lst)

	return final_str

'''
	Function to make tar file from a directory
'''
def make_tarfile(output_filename, source_dir):
	with tarfile.open(output_filename, "w:gz") as tar:
		tar.add(source_dir, arcname=os.path.sep)

if __name__ ==  '__main__':

	# Checking if command is valid
	if len(sys.argv)!=3:
		print("Please enter the command as below :")
		print("python clean_text.py [input file] [output file]")
		sys.exit(1)

	# Input -> JSON file
	if sys.argv[1][-4:] == 'json':
		file = open(sys.argv[1])
		data = json.load(file)
		cleaned_data = {}
		cleaned_data['impression'] = clean_text(data['impression'])
		with open(sys.argv[2], 'w') as f:
			json.dump(cleaned_data, f)

	# Input -> csv file
	elif sys.argv[1][-4:] == '.csv':
		with open(sys.argv[1]) as inputfile, open(sys.argv[2],'w+',newline='') as outfile:
			
			files = csv.reader(inputfile, delimiter=',')
			writer = csv.writer(outfile, delimiter=',')
			for i,row in enumerate(files):
				filename, impression = row
				if i == 0:
					writer.writerow([filename, impression])
				else:
					writer.writerow([filename, clean_text(impression)])


	# Input -> tarfile
	elif sys.argv[1][-7:-3] == '.tar':
		with tarfile.open(sys.argv[1]) as inputfile, tarfile.open(sys.argv[2], 'w:gz') as outfile:
			filenames = inputfile.getnames()
			cwd = os.getcwd() + '/temp'

			# Creating a temporary directory to store the output JSON files
			if not os.path.exists(cwd):
				os.makedirs(cwd)

			for filename in filenames:
				print(filename)
				file = inputfile.extractfile(filename).read()
				data = json.loads(file)
				cleaned_data = {"impression":clean_text(data['impression'])}
				with open(cwd+'/'+filename, 'w') as f:
					json.dump(cleaned_data, f)

		# Converting the temp directory into a tar file and deleting the temp folder
		make_tarfile(os.getcwd()+'/'+sys.argv[2], cwd)
		shutil.rmtree(cwd)

	# Input -> pickle file
	elif sys.argv[1][-4:] == '.pkl':
		with open(sys.argv[1],'rb') as inputfile, open(sys.argv[2],'wb') as outfile:
			file = pickle.load(inputfile)
			cleaned_data = []
			for data in file:
				cleaned_data.append({'impression':clean_text(data['impression'])})
			pickle.dump(cleaned_data, outfile)
		infile = open(sys.argv[2],'rb')
		new_dict = pickle.load(infile)
		infile.close()

	# If input is of uknown format
	else:
		print("This file only supports csv, tar and pkl files")
		sys.exit(1)