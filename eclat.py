
import numpy as np
from tkinter import *
import tracemalloc

def viewProgress(data, text_area):
	text_area.configure(state='normal')
	text_area.insert(INSERT, data+'\n')
	text_area.configure(state='disabled')

def compute_vertical_bitvector_data(data, text_area):
	#---build item to idx mapping---#
	idx = 0
	item2idx = {}
	for transaction in data:
		for item in transaction:
			if not item in item2idx:
				item2idx[item] = idx
				idx += 1
	idx2item = { idx : str(int(item)) for item, idx in item2idx.items() }
	#---build vertical data---#
	vb_data = np.zeros((len(item2idx), len(data)), dtype=int)
	for trans_id, transaction in enumerate(data):
		for item in transaction:
			vb_data[item2idx[item], trans_id] = 1
	viewProgress('Data transformed into vertical bitvector representation with shape: '+str(np.shape(vb_data)), text_area)
	return vb_data, idx2item

def compute_L1(data, idx2item, num_trans, min_support):
	L1 = []
	support_list = {}
	for idx, bit_list in enumerate(data):
		support = np.sum(bit_list) / num_trans
		if support >= min_support:
			support_list[frozenset([idx2item[idx]])] = bit_list
			L1.append([idx2item[idx]])
	return list(map(frozenset, sorted(L1))), support_list

def compute_LK(LK_, support_list, k, num_trans, min_support):
	LK = []
	supportK = {}
	for i in range(len(LK_)):
		for j in range(i+1, len(LK_)):  # enumerate all combinations in the Lk-1 itemsets
			L1 = sorted(list(LK_[i])[:k-2])
			L2 = sorted(list(LK_[j])[:k-2])
			if L1 == L2: # if the first k-1 terms are the same in two itemsets, calculate the intersection support
				union = np.multiply(support_list[LK_[i]], support_list[LK_[j]])
				union_support = np.sum(union) / num_trans
				if union_support >= min_support:
					new_itemset = frozenset(sorted(list(LK_[i] | LK_[j])))
					if new_itemset not in LK:
						LK.append(new_itemset)
						supportK[new_itemset] = union
	return sorted(LK), supportK


	def get_result(self):
		viewProgress("", self.text_area)
		return self.support_list

def output_handling(support_list):
	L = []
	for itemset, count in sorted(support_list.items(), key=lambda x: len(x[0])):
		itemset = tuple(sorted(list(itemset), key=lambda x: int(x)))
		if len(L) == 0:
			L.append([itemset])
		elif len(L[-1][0]) == len(itemset):
			L[-1].append(itemset)
		elif len(L[-1][0]) != len(itemset):
			L[-1] = sorted(L[-1])
			L.append([itemset])
		else: raise ValueError()
	if len(L) != 0: L[-1] = sorted(L[-1])
	L = tuple(L)
	support_list = dict((tuple(sorted(list(k), key=lambda x: int(x))), v) for k, v in support_list.items())
	return L, support_list


def eclat(data, min_support, iterative=True, text_area=None):
	tracemalloc.start()
	num_trans = float(len(data))
	
	#---iterative method---#
	if iterative:

		vb_data, idx2item = compute_vertical_bitvector_data(data, text_area=text_area)
		L1, support_list = compute_L1(vb_data, idx2item, num_trans, min_support)
		L = [L1]
		k = 1
		
		while True:
			viewProgress('Menjalankan Algoritma Eclat: Iterasi ke- '+str(k)+' dengan '+str(len(L[-1]))+' itemsets in L'+str(k)+'...', text_area)
			k += 1
			LK, supportK = compute_LK(L[-1], support_list, k, num_trans, min_support)

			if len(LK) == 0:
				L = [sorted([tuple(sorted(itemset)) for itemset in LK]) for LK in L]
				support_list = dict((tuple(sorted(k)), np.sum(v)) for k, v in support_list.items())
				viewProgress('Menjalankan Algoritma Eclat: Iterasi ke- '+str(k-1)+'-th. Terminating ...', text_area)
				break
			else:
				L.append(LK)
				support_list.update(supportK)
		viewProgress("----------------------------------------------------------------------",text_area)
		current, peak = tracemalloc.get_traced_memory()
		viewProgress(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB",text_area)
		tracemalloc.stop()
		return L, support_list
