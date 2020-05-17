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


def generate(obj=10, ppl=5):
    # set ITEM := 1 2 3 4;
    str1 = "set ITEMS :="
    for i in range(obj):
        str1 += " {}".format(i+1)
    str1 += ';\n'

    # set PEOPLE := 1 2 3 4;
    str2 = "set PEOPLE :="
    for i in range(ppl):
        str2 += " {}".format(i+1)
    str2 += ';\n \n'

    # param values: 1 2 3 4 :=

    str3 = "param values:"
    for i in range(obj):
        str3 += " {}".format(i+1)
    str3 += ':='

    heuristic = []
    for i in range(obj):
        heuristic.append(random.randint(1, 1000))

    str4 = ""
    for i in range(ppl):
        str4 += "\n{}".format(i+1)
        for j in range(obj):
            x = heuristic[j]
            str4 += " {}".format(x + random.randint(0, (x//5)))
    str4 += ';'
    str4

    filename = "/Users/jonathan/Desktop/random_data/{}ppl{}obj_heuristic".format(ppl, obj)
    filename += ".dat"

    file = open(filename, "w")
    file.write(str1)
    file.write(str2)
    file.write(str3)
    file.write(str4)
    file.close()

def run_one_experiment(ampl, obj = 5, ppl = 5):
	generate(obj = obj, ppl = ppl,)
	ampl.reset()
	ampl.read('/Users/jonathan/Desktop/169projectPEnvy.mod')
	ampl.readData("/Users/jonathan/Desktop/random_data/{}ppl{}obj_heuristic.dat".format(ppl, obj))
	ampl.setOption('solver', 'cplex')
	start_time = time.time()
	ampl.solve()
	finish_time = time.time()
	p_envy = ampl.getObjective('p_envy').value()
		
	return p_envy, finish_time-start_time

ampl = AMPL(Environment("/Users/jonathan/Documents/files/amplide.macosx64/amplide.macosx64"))

with open('part4.csv', 'a', newline='') as csvfile:
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