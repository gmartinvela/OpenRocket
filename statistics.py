import fileinput
import math
import time
import numpy as np
from pylab import *
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd

# 1-51, 1-301, 1-5801

#file_path = '/media/ABB4-4F3A/DATALOG.TXT'
file_path = 'DATALOG.TXT'
headers = {
	'ax': 'acceleration in X', 'ay': 'acceleration in Y', 'az': 'acceleration in Z',
	'mx': 'magnetoscope in X', 'my': 'magnetoscope in Y', 'mz': 'magnetoscope in Z',
	'gx': 'gyroscope in X', 'gy': 'gyroscope in Y', 'gz': 'gyroscope in Z',
	'f': 'timestamp', 't': 'temperature', 'p': 'pressure', 'h': 'altitude (meters)'
}

def retrieve_string_now():
        '''
        Retrieve the time since epoch
        Return: time since epoch multiplied by 100 to do it integer
        '''        
        now = time.time()
        now = int(now * 100)
        string_now = str(now)
        return string_now

def txt_to_dataframes(txt_file, pattern):
	'''
	Find all the blocks generated by the rocket and convert it to dataframes
	Return: Dataframes containing all the different blocks of data in the .txt file
	'''
	num_times_find_pattern = []
	for num_line, line in enumerate(fileinput.input(txt_file)):
		if pattern in line:
			num_times_find_pattern.append(num_line)	
	max_num_line = max(enumerate(fileinput.input(txt_file)))
	num_times_find_pattern.append(max_num_line[0])
	#print num_times_find_pattern
	num_lines_list = []
	for num_line in num_times_find_pattern:
		if num_line == 0:
			num_prev = num_line
		else:
			num_lines_list.append(num_line - num_prev)
			num_prev = num_line
	num_lines_list[-1] = num_lines_list[-1] + 1
	#print num_lines_list
	dataframes = []
	reader = pd.read_table(file_path, sep=',', iterator=True)
	for num_line in num_lines_list:
		if num_line != 1:
			dataframe = reader.get_chunk(num_line)
			#dataframe = dataframe.dropna()
			dataframe = dataframe.drop(dataframe.index[-1])
			dataframes.append(dataframe)
			#print dataframe.head(2)
			#print dataframe.tail(2)
		else:
			dataframe = reader.get_chunk(num_line)
	return dataframes

def extract_valid_launches(dataframes, min_milliseconds_launch = 8000, milliseconds_write_cycle_mean = 23):
	'''
	Find the valid launches generated by the rocket
	Params:
		min_milliseconds_launch = 8000. By default each launch it is supposed to take 8 seconds minimum
		milliseconds_write_cycle_mean = 23. By default each Arduino write cycle is 23 milliseconds
	Return: Valid dataframes with real launches
	'''
	# minimum entries by default will be 347 = 8000 / 23
	minimum_entries = int(min_milliseconds_launch / milliseconds_write_cycle_mean)
	valid_dataframes = []
	for dataframe in dataframes:
		if len(dataframe.index) > minimum_entries:
			valid_dataframes.append(dataframe)
	return valid_dataframes

def save_altitude_time_basic(dataframe):
	now = retrieve_string_now()
	MAX = dataframe.h.max()
	MIN = dataframe.h.min()
	# Comment the line below if you want a default image
	# If you dont comment you will have a bigger image but the processing time will increase
	fig = figure(1, figsize=(16, 12))
	plt.plot(dataframe.f, dataframe.h, linewidth=1.0, color="blue")
	plt.axhline(0, color='black', lw=2)
	xlabel('Time (milliseconds)', fontsize = 10)
	ylabel(headers['h'], fontsize = 10)
	title('%s from the launch platform' % headers['h'], fontsize=12)
	#main_legend = legend(['Altitude over the time'], loc='upper right', shadow=True)
	data_legend = legend(['MAX: %.2f\nMIN: %.2f' % (MAX, MIN)], loc=1)
	#gca().add_artist(main_legend)
	gca().add_artist(data_legend)
	grid(True)
	#image_path = '/home/gustavo/Desktop/OpenRocket/images/data/altitude_%s.png' % now 
	#plt.savefig(image_path, orientation='landscape', bbox_inches='tight', pad_inches=0)
	#plt.close()
	plt.show()

def save_altitude_pressure_time_basic(dataframe):
	now = retrieve_string_now()
	MAX = dataframe.h.max()
	MIN = dataframe.h.min()
	# make a little extra space between the subplots
	plt.subplots_adjust(wspace=0.1)

	plt.subplot(211)
	plt.plot(dataframe.f, dataframe.h, linewidth=1.0, color="blue")
	plt.axhline(0, color='black', lw=2)
	xlabel('Time (milliseconds)', fontsize = 10)
	ylabel(headers['h'], fontsize = 10)
	title('%s from the launch platform' % headers['h'], fontsize=12)
	#main_legend = legend(['Altitude over the time'], loc='upper right', shadow=True)
	data_legend = legend(['MAX: %.2f\nMIN: %.2f' % (MAX, MIN)], loc=1)
	#gca().add_artist(main_legend)
	gca().add_artist(data_legend)
	grid(True)

	plt.subplot(212)
	plt.plot(dataframe.f, dataframe.p, linewidth=1.0, color="blue")
	xlabel('Time (milliseconds)', fontsize = 10)
	ylabel(headers['p'], fontsize = 10)
	title('%s from the launch platform' % headers['p'], fontsize=12)
	grid(True)
	plt.show()

dataframes = txt_to_dataframes(file_path, "m")
valid_dataframes = extract_valid_launches(dataframes)
#print valid_dataframes[0].tail(3)
for dataframe in valid_dataframes:
	save_altitude_pressure_time_basic(dataframe)