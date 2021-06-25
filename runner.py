# -*- coding: utf-8 -*- #
"""*********************************************************************************************"""
#   FileName     [ runner.py ]
#   Synopsis     [ Implement of two basic algorithms to perform frequent pattern mining: 1. Apriori, 2. Eclat. 
#   			   Find all itemsets with support > min_support. ]
#   Author       [ Ting-Wei Liu (Andi611) ]
#   Copyright    [ Copyleft(c), NTUEE, NTU, Taiwan ]
"""*********************************************************************************************"""


###############
# IMPORTATION #
###############
import os
import tracemalloc
import csv
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import filedialog
#-----------------------------#
from apriori import apriori
from eclat import eclat
#-----------------------#
plt.switch_backend('agg')
plt.rcParams.update({'figure.max_open_warning': 0})


##################
# CONFIGURATIONS #
##################
# Not use if using GUI
def get_config():
	parser = argparse.ArgumentParser(description='frequent itemset mining argument parser')
	# parser.add_argument('mode', type=str, choices=['apriori', 'eclat', '1', '2'], help='algorithm mode')
	parser.add_argument('--min_support', type=float, default=0.6, help='minimum support of the frequent itemset')
	parser.add_argument('--toy_data', action='store_true', help='use toy data for testing')
	parser.add_argument('--iterative', action='store_true', help='run eclat in iterative method, else use the recusrive method')
	
	io_parser = parser.add_argument_group('IO settings')
	io_parser.add_argument('--input_path', type=str, default='./data/data.txt', help='input data path')
	io_parser.add_argument('--output_path', type=str, default='./data/output.txt', help='output data path')
	args = parser.parse_args()
	# if args.mode == '1': args.mode = 'apriori'
	# elif args.mode == '2': args.mode = 'eclat'
	return args



###############
# View Result #
###############
def viewProgress(data):
	global text_area
	text_area.configure(state='normal')
	text_area.insert(INSERT, data+'\n')
	text_area.configure(state='disabled')


	

#############
# READ DATA #
#############
def read_data(data_path, skip_header=False, toy_data=False):
	if toy_data:
		return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
	data = []
	if not os.path.isfile(data_path): raise ValueError('Invalid data path.')
	with open(data_path, 'r', encoding='utf-8') as f:
		file = csv.reader(f, delimiter=' ', quotechar='\r')
		if skip_header: next(file, None)  # skip the headers
		for row in file:
			data.append(row)
	return data


#################
# RUN ALGORITHM #
#################
def run_algorithm(data, mode, support, iterative):
	global text_area
	iterative = True
	if mode == 'apriori':
		viewProgress('Running Apriori algorithm with '+str(support)+' support and data shape: '+str(np.shape(data)))
		result = apriori(data, support, text_area)
		return result
	elif mode == 'eclat':
		viewProgress('Running Eclat algorithm with '+str(support)+' support and data shape: '+str(np.shape(data)))
		result = eclat(data, support, iterative, text_area)

		return result
	else:
		raise NotImplementedError('Invalid algorithm mode.')


################
# WRITE RESULT #
################
def write_result(result, result_path):
	if len(result[0]) == 0: viewProgress('Found 0 frequent itemset, please try again with a lower minimum support value!')
	with open(result_path, 'w', encoding='big5') as file:
		file_data = csv.writer(file, delimiter=',', quotechar='\r')
		for itemset_K in result[0]:
			for itemset in itemset_K:
				output_string = ''
				for item in itemset: output_string += str(item)+' '
				output_string += '(' + str(result[1][itemset]) +  ')'
				file_data.writerow([output_string])

	viewProgress('Results have been successfully saved to: '+str(result_path))
	return True
def assert_at_most_one_is_true(*args):
    return sum(args) <= 1

########
# MAIN #
########
"""
	main function that runs the two algorithms, 
	and plots different experiment results.
"""
def main(root):
	global text_area
	
	args = get_config()
	data = read_data(inFile.get(), toy_data=args.toy_data)
	label_frame5 = LabelFrame(root, text="Hasil", width=50)
	label_frame5.grid(column=3, row=1, sticky=W,rowspan=4)
	text_area.grid_forget()
	text_area = st.ScrolledText(label_frame5, width=60, height=17, font=("Times New Roman", 10))
	text_area.grid(column=3, row=0, rowspan=8, padx=5)
	text_area.configure(state='disabled')
		
	duration = []
	start_time = time.time()
	result = run_algorithm(data, alg.get(), float(minsup.get()), args.iterative)
	"""
	result has len()==2, 
	result[0]: the 3-dimensional Large K itemset,
	result[1]: the dictionary storing the support of each itemset
	"""
	duration.append(time.time() - start_time)
	viewProgress("Execution Time: "+str(duration[-1])[:7])

	done = write_result(result, outFile.get())


def inF(root):
	global pathinFile
	root.filename = filedialog.askopenfilename(initialdir="", title="Choose input file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
	pathinFile = str(root.filename)
	inFile.insert(0, pathinFile)

def outF(root):
	global pathoutFile
	saveTo = filedialog.asksaveasfile(initialdir="", title="Choose output file", filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
	pathoutFile = str(saveTo.name)
	outFile.insert(0, pathoutFile)

def clear_text():
   inFile.delete(0, END)
   outFile.delete(0, END)
   minsup.delete(0, END)
   text_area.delete(0, END)

def gui(root):
	global inFile, outFile, text_area, minsup, alg, gpu_status



	root.title("APLIKASI ASSOCIATION RULES MINING")
	root.resizable(0,0)
	label = Label(root,text="APLIKASI ASSOCTIATION RULES MINING",font='Impact', bg='#5c85ff',fg='white', width=96, height=1)
	
	


	label_frame = LabelFrame(root, text="Pilih Metode", width=50)
	label_frame2 = LabelFrame(root, text="Dataset", width=50)
	label_frame3 = LabelFrame(root, text="Minimum Support", width=50)
	label_frame4 = LabelFrame(root, text="Aksi", width=50)
	label_frame5 = LabelFrame(root, text="Hasil", width=50)

	alg_Lb = Label(label_frame, text="PILIH ALGORITMA :")
	inFile_Lb = Label(label_frame2, text="PILIH DATASET :")
	outFile_Lb = Label(label_frame2, text="SIMPAN RULES :")
	minsup_Lb = Label(label_frame3, text="MINIMUM SUPPORT (%) :")
	alg = StringVar()
	alg.set('apriori')
	dropDown = OptionMenu(label_frame, alg, 'apriori', 'eclat')
	dropDown.config(width=29)
	inFile = Entry(label_frame2, width=35)
	outFile = Entry(label_frame2, width=35)
	minsup = Entry(label_frame3, width=25)
	inFile_Btn = Button(label_frame2, text="...", command=lambda: inF(root))
	outFile_Btn = Button(label_frame2, text="...", command=lambda: outF(root))
	minsup_Lb_end = Label(label_frame3, text="(Contoh : 0.6)")

	label_frame.grid(column=0, row=1, sticky=W,columnspan=2,padx=10)
	label_frame2.grid(column=0, row=2, sticky=W,columnspan=2,padx=10)
	label_frame3.grid(column=0, row=3, sticky=W,columnspan=2,padx=10)
	label_frame4.grid(column=0, row=4, sticky=W,columnspan=2,padx=10)
	label_frame5.grid(column=3, row=1, sticky=W,rowspan=4)
	label.grid(column=0,row=0, columnspan=4)
	alg_Lb.grid(column=0, row=1, sticky=W)
	inFile_Lb.grid(column=0, row=2, sticky=W)
	outFile_Lb.grid(column=0, row=3, sticky=W)
	minsup_Lb.grid(column=0, row=4, sticky=W)
	dropDown.grid(column=1, row=1, sticky=W,pady=5,padx=5)
	inFile.grid(column=1, row=2,sticky=W)
	outFile.grid(column=1, row=3,sticky=W)
	minsup.grid(column=1, row=4, sticky=W)
	inFile_Btn.grid(column=2, row=2, pady=5,padx=5, sticky=E)
	outFile_Btn.grid(column=2, row=3, sticky=E,pady=5,padx=5)
	minsup_Lb_end.grid(column=1, row=4, sticky=E,pady=5)

	# blank
	blank1 = Label(root)
	blank1.grid(column=0, row=5, columnspan=3)

	
	startBtn = Button(label_frame4, text="Run algorithm",width=30, command=lambda: main(root))
	blank3 = Label(root, text="")
	button_clear = Button(label_frame4,text="Clear", command=clear_text, font=('Helvetica bold',10),width=10).grid(column=2, row=6, sticky=E, pady=5, padx=10)

	
	startBtn.grid(column=1, row=6, sticky=W, pady=10,padx=5)
	
	

	text_area = st.ScrolledText(label_frame5, width=60, height=17, font=("Times New Roman", 10))
	text_area.grid(column=3, row=0, rowspan=8, padx=5)
	text_area.configure(state='disabled')

	# Check GPU
	import eclat
	
	

	root.mainloop()

gui(Tk())
# if __name__ == '__main__':
# 	main()

