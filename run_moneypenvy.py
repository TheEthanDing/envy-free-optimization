from __future__ import print_function, absolute_import, division

import numpy as np
import pandas as pd
import random
import os
import csv

from builtins import map, range, object, zip, sorted
import sys
import os
from amplpy import AMPL, Environment
import time

def generate(obj = 5, ppl = 5, cash=1):
	#set ITEM := 1 2 3 4;
	str1 = "set ITEMS :="
	for i in range(obj):
		str1 += " {}".format(i+1)
	str1 += ';\n'

	#set PEOPLE := 1 2 3 4;
	str2 = "set PEOPLE :="
	for i in range(ppl):
		str2 += " {}".format(i+1)
	str2 += ';\n \n'

	#param values: 1 2 3 4 := 

	str3 = "param values:"
	for i in range(obj):
		str3 += " {}".format(i+1)
	str3 += ':='

	str4 = ""
	for i in range(ppl):
		str4 += "\n{}".format(i+1)
		for i in range(obj):
			str4 += " {}".format(random.random())
	str4 += ';'
	str4 += '\n \n'

	str5 = f"param cash := {cash};"

	filename = "/Users/jonathan/Desktop/random_data/{}ppl{}obj".format(ppl, obj)
	filename += ".dat"

	file = open(filename, "w") 
	file.write(str1) 
	file.write(str2)
	file.write(str3)
	file.write(str4)
	file.write(str5)
	file.close()


def run_one_experiment(ampl, obj = 5, ppl = 5, cash=0.25):
	generate(obj = obj, ppl = ppl, cash = cash)
	ampl.reset()
	ampl.read('/Users/jonathan/Desktop/penvy_with_cash.mod')
	ampl.readData("/Users/jonathan/Desktop/random_data/{}ppl{}obj.dat".format(ppl, obj))
	ampl.setOption('solver', 'cplex')
	start_time = time.time()
	ampl.solve()
	finish_time = time.time()
	p_envy = ampl.getObjective('p_envy').value()
		
	return p_envy, finish_time-start_time

ampl = AMPL(Environment("/Users/jonathan/Documents/files/amplide.macosx64/amplide.macosx64"))

with open('money_penvy_0.25_good.csv', 'a', newline='') as csvfile:
	fieldnames = ['Number of People', 'Number of Items', 'Optimal P-Envy', 'Wall Clock Time']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(1,11):
		for j in range(1,11):
			for _ in range(30):
				p_envy, run_time = run_one_experiment(ampl, i, j)
				out = {'Number of People': j, 
						'Number of Items': i, 
						'Optimal P-Envy': p_envy, 
						'Wall Clock Time': run_time}
				print(out)
				writer.writerow(out)
				csvfile.flush()