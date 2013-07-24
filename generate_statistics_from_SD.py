import fileinput
import time

file_path = '/media/ABB4-4F3A/DATALOG.TXT'

def split_in_blocks(txt_file, pattern):
	'''
	Find the last appears of the text that indicate a new flight and divide in the number of blocks generated by the rocket
	Return: A list that contains all the different blocks of data and a list containing the header.
	'''
	num_times_find_pattern = []
	for num_line, line in enumerate(fileinput.input(txt_file)):
		if pattern in line:
			num_times_find_pattern.append(num_line)
		if num_line == 0:
			header = list(line.strip().split(","))
			print header
	blocks_of_data = []
	with open(txt_file) as f:
		lines = f.readlines()
		for num_header_line in num_times_find_pattern: 
			if num_header_line == 0:
				num_header_line_prev = num_header_line
			else:
				block_lines = lines[num_header_line_prev + 1 : num_header_line - 1]
				blocks_of_data.append(block_lines)
				num_header_line_prev = num_header_line
		block_lines = lines[num_header_line_prev + 1 : num_line + 1]
		blocks_of_data.append(block_lines)
	return blocks_of_data, header

def manage_data_from_blocks(blocks, header):
	'''
	Divide al the text in blocks tagged with their type of data (accelaration, temperature, ...) continued by a number of block
	Return: A dict that contains all the different types of data diferentiated and numbered.
	'''
	blocks_dict = {}
	for block_number, block in enumerate(blocks):
		blocks_dict['m%s' % block_number] = []
		blocks_dict['ax%s' % block_number] = []
		blocks_dict['ay%s' % block_number] = []
		blocks_dict['az%s' % block_number] = []
		blocks_dict['gx%s' % block_number] = []
		blocks_dict['gy%s' % block_number] = []
		blocks_dict['gz%s' % block_number] = []
		blocks_dict['mx%s' % block_number] = []
		blocks_dict['my%s' % block_number] = []
		blocks_dict['mz%s' % block_number] = []
		blocks_dict['t%s' % block_number] = []
		blocks_dict['p%s' % block_number] = []
		blocks_dict['al%s' % block_number] = []
		for line in block:
			line_list = line.strip().split(",")
			#print line_list
			m_list = int(line_list[0])
			ax_list = float(line_list[1])
			ay_list = float(line_list[2])
			az_list = float(line_list[3])
			gx_list = float(line_list[4])
			gy_list = float(line_list[5])
			gz_list = float(line_list[6])
			mx_list = float(line_list[7])
			my_list = float(line_list[8])
			mz_list = float(line_list[9])
			t_list = float(line_list[10])
			p_list = int(line_list[11])
			al_list = float(line_list[12])
			#print timestamp_list
			blocks_dict['t%s' % block_number].append(m_list)
			blocks_dict['ax%s' % block_number].append(ax_list)
			blocks_dict['ay%s' % block_number].append(ay_list)
			blocks_dict['az%s' % block_number].append(az_list)
			blocks_dict['gx%s' % block_number].append(gx_list)
			blocks_dict['gy%s' % block_number].append(gy_list)
			blocks_dict['gz%s' % block_number].append(gz_list)
			blocks_dict['mx%s' % block_number].append(mx_list)
			blocks_dict['my%s' % block_number].append(my_list)
			blocks_dict['mz%s' % block_number].append(mz_list)
			blocks_dict['t%s' % block_number].append(t_list)
			blocks_dict['p%s' % block_number].append(p_list)
			blocks_dict['al%s' % block_number].append(al_list)
	return blocks_dict

def process_data(concrete_blocks_dict):
	millis_processed = []
	for position, millis in enumerate(concrete_blocks_dict):
		millis_interval_list = []
		if position != 0:
			millis_interval = millis - millis_prev
			#print millis_interval
			millis_interval_list.append(millis_interval)
		millis_prev = millis
		millis_average = sum(millis_interval_list) / position
		millis_max = max(millis_interval_list)
		millis_min = min(millis_interval_list)
		print "Interval: ",millis_interval
		print "MAX: ",millis_max
		print "MIN: ",millis_min



#start = time.time()
blocks, header = split_in_blocks(file_path, "m")
blocks_dict = manage_data_from_blocks(blocks, header)
#for key in sorted(blocks_dict.iterkeys()):
#		print "%s" % key


#stop = time.time()
#total_time = stop -start
#print total_time