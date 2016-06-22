#!/usr/bin/env python

import re, codecs
import numpy as np
from decimal import Decimal
import random

def runfraction(run):
	if int(run) > 400:
		return 1.0
	else:
		return float(run) / 400
def average(run,wicket):
	if wicket == "0":
		return float(run)
	else:
		return float(run) / float(wicket)
def strikerate(run,balls):
	return float(run) / float(balls)
# function first_member converst the input string to a 50 member list having numbers instead of letters. Conversion depends on mode ASCII / Sanskrit.
def first_member(datatuple):
    bigval = []
    for (run,average,strikerate,winner) in datatuple:
        bigval.append((run,average,strikerate))
    return bigval

# function second_member converts the name of the class to its index in all_class_types. Thus the second member is also converted to numbers to be manipulatable for network.
def second_member(datatuple):
    secval = []
    for (run,average,strikerate,winner) in datatuple:
        secval.append(winner)
    return secval
def returnwinner(team,winner):
	if team == winner:
		return 1
	else:
		return 0
def normalize(lst):
	output = []
	maximum = float(max(lst))
	minimum = float(min(lst))
	for observation in lst:
		observation = float(observation)
		output.append((observation-minimum) / (maximum-minimum))
	return output


def readcsv(inputfile,outputfile):
	output = []
	fout = codecs.open(outputfile,'w','utf-8')
	for line in codecs.open(inputfile, 'r','utf-8'):
		line = line.strip()
		#Australia,377,6,305,South Africa,294,10,296,runs,83,Australia
		[team1,run1,wicket1,ball1,team2,run2,wicket2,ball2,winmethod,winby,winner] = line.split(',')
		run1 = float(run1)
		run2 = float(run2)
		average1 = average(run1,wicket1)
		average2 = average(run2,wicket2)
		strikerate1 = strikerate(run1,ball1)
		strikerate2 = strikerate(run2,ball2)
		winnernum1 = returnwinner(team1,winner)
		winnernum2 = returnwinner(team2,winner)
		output.append((run1,average1,strikerate1,winnernum1))
		output.append((run2,average2,strikerate2,winnernum2))
		fout.write(str(run1)+','+str(average1)+','+str(strikerate1)+','+str(winnernum1)+'\n')
		fout.write(str(run2)+','+str(average2)+','+str(strikerate2)+','+str(winnernum2)+'\n')	
	fout.close()

def writenormalizer(inputcsvfile,normalizedtxtfile):
	datatuple = []
	for line in codecs.open(inputcsvfile,'r','utf-8'):
		line = line.strip()
		[p,q,r,s] = line.split(',')
		datatuple.append((p,q,r,s))
	runs = [float(a) for (a,b,c,d) in datatuple]
	average = [b for (a,b,c,d) in datatuple]
	strikerate = [c for (a,b,c,d) in datatuple]
	winstatus = [int(d) for (a,b,c,d) in datatuple]
	runa = normalize(runs)
	averagea = normalize(average)
	strikeratea = normalize(strikerate)
	output = []
	fout = codecs.open(normalizedtxtfile,'w','utf-8')
	for i in xrange(len(datatuple)):
		#print runa[i], averagea[i], strikeratea[i], winstatus[i]
		output.append((runa[i],averagea[i],strikeratea[i],winstatus[i]))
		fout.write(str(runa[i])+','+str(averagea[i])+','+str(strikeratea[i])+','+str(winstatus[i])+'\n')
	fout.close()
	return output

# function loadable_data is the function which splits the given input data and output data into two parts - 80% training data and 20% evaluation data. The data are in numpy ndarray format. This is the format in which the load_data_wrapper code takes input. Now our data is compatible with the system of original code by M Neilson.
def loadable_data(datatuple):
    x = np.array(first_member(datatuple[0:(len(datatuple)*2/10)]))
    y = np.array(second_member(datatuple[0:(len(datatuple)*2)/10]))
    x1 = np.array(first_member(datatuple[(len(datatuple)*2)/10:]))
    y1 = np.array(second_member(datatuple[(len(datatuple)*2)/10:]))
    return ((x,y),(x1,y1))
# Change in function is addition of parameter output_neuron to make it extensible to any class numbers.
def vectorized_result(j, output_neuron):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  This is used to convert a digit
    (0...9) into a corresponding desired output from the neural
    network."""
    e = np.zeros((output_neuron, 1))
    e[j] = 1.0
    return e
# Change in the function is addition of two parameters output_neuron and mode to suit string manipulation.
def load_data_wrapper(datatuple):
    tr_d, te_d = loadable_data(datatuple)
    training_inputs = [np.reshape(x, (3, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y, 2) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    test_inputs = [np.reshape(x, (3, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, test_data)

#readcsv('data.csv','data1.csv')
datatuple = writenormalizer('data1.csv','normalized.txt')
input_neuron = 3
intermediate_neuron = 30
output_neuron = 2
epochs = 1000
mini_batch_size = 10
eta = 1.0
lmbda = 0.5
monitor_evaluation_cost = True
monitor_evaluation_accuracy = True
monitor_training_cost = True
monitor_training_accuracy = True
howmany = 1
