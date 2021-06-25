def compute_C1_and_L1_itemset(data, num_trans, min_support):
	C1 = {}
	for transaction in data:
		for item in transaction:
			if not item in C1:
				C1[item] = 1
			else: C1[item] += 1
	L1 = []
	support1 = {}
	for candidate, count in sorted(C1.items(), key=lambda x: x[0]):
		support = count / num_trans
		if support >= min_support:
			L1.insert(0, [candidate])
			support1[frozenset([candidate])] = count
	return list(map(frozenset, sorted(L1))), support1, C1

def compute_CK(LK_, k):
	CK = []
	for i in range(len(LK_)):
		for j in range(i+1, len(LK_)):
			L1 = sorted(list(LK_[i]))[:k-2]
			L2 = sorted(list(LK_[j]))[:k-2]
			if L1 == L2:
				new_candidate = frozenset(sorted(list(LK_[i] | LK_[j])))
				CK.append(new_candidate) 
	return sorted(CK)

def compute_LK(D, CK, num_trans, min_support):
	support_count = {}
	for item in D:
		for candidate in CK:
			if candidate.issubset(item):
				if not candidate in support_count:
					support_count[candidate] = 1
				else: support_count[candidate] += 1
	LK = []
	supportK = {}
	for candidate, count in sorted(support_count.items(), key=lambda x: x[0]):
		support = count / num_trans
		if support >= min_support:
			LK.append(candidate)
			supportK[candidate] = count
	return sorted(LK), supportK

from tkinter import *
import tracemalloc

def viewProgress(data, text_area):
	text_area.configure(state='normal')
	text_area.insert(INSERT, data+'\n')
	text_area.configure(state='disabled')

def apriori(data, min_support, text_area):
	tracemalloc.start()
	D = sorted(list(map(set, data)))
	num_trans = float(len(D))
	L1, support_list, CK = compute_C1_and_L1_itemset(data, num_trans, min_support)
	L = [L1]
	k = 1

	while (True):
		viewProgress('Menjalankan Algoritma Apriori: Iterasi ke-'+str(k)+' dengan '+str(len(CK))+' candidates...', text_area)
		k += 1
		CK = compute_CK(LK_=L[-1], k=k)
		LK, supportK = compute_LK(D, CK, num_trans, min_support)
		if len(LK) == 0: 
			L = [sorted([tuple(sorted(list(itemset), key=lambda x: int(x))) for itemset in LK]) for LK in L]
			support_list = dict((tuple(sorted(list(k), key=lambda x: int(x))), v) for k, v in support_list.items())
			viewProgress('Menjalankan Algoritma Apriori: Iterasi ke- '+str(k-1)+'. Terminating ...', text_area)
			break
		else:
			L.append(LK)
			support_list.update(supportK)
	viewProgress("--------------------------------------------------------------------------------------",text_area)
	current, peak = tracemalloc.get_traced_memory()
	viewProgress(f"Memory yang digunakan saat ini {current / 10**6}MB; Penggunaan Memory Maksimum {peak / 10**6}MB",text_area)
	tracemalloc.stop()
	return L, support_list

