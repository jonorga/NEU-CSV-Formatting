import csv
import os

# Scan all files in folder
arr = os.listdir()
raw_data = []
total_files = 0

# Find raw data files
for fileNames in arr:
	if fileNames.endswith(".csv"):
		if fileNames.startswith('NAV'):
			if fileNames.startswith('NAVIGATE'):
				this_variable_goes_to_nothing_and_does_nothing = 0
			else:
				total_files += 1
				raw_data.append(fileNames)

print('Total files:', total_files)
successfully_formatted = []
no_data_found = []
unable_to_format = []

for raw_files in raw_data:
	RPE = ['NaN']*30
	rpe_counter = 0
	JS = ['NaN']*30
	js_counter = 0
	code_correct = ['NaN']*30
	code_correct_counter = 0
	code_given = ['NaN']*30
	code_given_counter = 0
	test_result = ['NaN']*30
	test_result_counter = 0
	confidence_given = ['NaN']*30
	confidence_given_counter = 0
	max_hr = 'NaN'
	date = 'NaN'
	hour_min = 'NaN'

	checkpoints_reached = 0
	checkpoints_correct = 0

	file_length = 0

	with open(raw_files, newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		# Read through file to make sure there's more than one line of info
		for row in spamreader:
			if row != "":
				file_length += 1

		if file_length > 1:
			try:
				csvfile.seek(0)		
				time = next(spamreader)
				time = time[0]
				max_hr = next(spamreader)
				if max_hr[0] == 'Max Heart Rate':
					max_hr = max_hr[1]
				else:
					max_hr = 'NaN'
				parsed_time = time.split(' ')
				if len(parsed_time) > 1:
					date = parsed_time[0]
					hour_min = parsed_time[1]
				for row in spamreader:
					if row[2] == 'Physical exertion':
						RPE[rpe_counter] = row[3]
						rpe_counter += 1
					if row[2] == 'Experience quality':
						JS[js_counter] = row[3]
						js_counter += 1
					if row[1] == 'New Task':
						holder = row[2]
						offset_int = int(holder[-1])
						code_correct[code_correct_counter] = row[2 + offset_int]
						code_correct_counter += 1
						checkpoints_reached += 1
					if row[1] == 'Answer given':
						if row[2] == 'Correct':
							test_result[test_result_counter] = 1
							test_result_counter += 1
							temp_holder = row[3]
							code_given[code_given_counter] = temp_holder[9:]
							code_given_counter += 1
							checkpoints_correct += 1
						if row[2] == 'Incorrect':
							test_result[test_result_counter] = 0
							test_result_counter += 1
							code_given[code_given_counter] = row[5]
							code_given_counter += 1
					if row[1] == 'Answer confidence':
						confidence_given[confidence_given_counter] = row[2]
						confidence_given_counter += 1

					last_row = row[0]

				parsed_name = raw_files.split('_')
				PID = parsed_name[0]
				PID = PID[3:]
				session_num = parsed_name[1]
				session_num = session_num[1:]
				condition_raw = parsed_name[2]
				if (condition_raw[0] == 'O'):
					condition = 'E'
				else:
					condition = 'T'
				condition += condition_raw[1]
				map_num = condition_raw[2]
				
				output_file_name = 'NAVIGATE_' + PID + '_' + session_num + '_' + condition + '.csv' 
				with open(output_file_name, 'w', newline='') as outputFile:
					spamwriter = csv.writer(outputFile, delimiter=',', quotechar='|')
					spamwriter.writerow(['Variable'] + ['Description'] + ['Example'])
					spamwriter.writerow(['PID'] + ['Participant ID Number (entered at start screen)'] + [PID])
					spamwriter.writerow(['Date'] + ['Date of Test'] + [date])
					spamwriter.writerow(['Start Time'] + ['Start Time of Test'] + [hour_min])
					spamwriter.writerow(['Session'] + ['Session Number (entered at start screen)'] + [session_num])
					spamwriter.writerow(['Condition'] + ['Condition (EN / TN / EU / TU) [E = Omni / T = Teleport]'] + [condition])
					spamwriter.writerow(['Map'] + ['Map Number'] + [map_num])
					spamwriter.writerow(['Session Time'] + ['Session Time of Test (last recorded event)'] + [last_row])
					i = 1
					while (i < 11):
						vari = 'RPE_' + str(i)
						desc = 'Physical exertion at ' + str(i*2) + ' minute mark'
						spamwriter.writerow([vari] + [desc] + [RPE[i-1]])
						i += 1
					j = 1
					while (j < 11):
						vari = 'JS_' + str(j)
						desc = 'Experience Quality at ' + str(j*2) + ' minute mark'
						spamwriter.writerow([vari] + [desc] + [JS[j-1]])
						j += 1

					k = 1
					while (k < 11):
						vari = 'CKPT_' + str(k) + '_CorrectAnswer'
						desc = 'Code at Checkpoint ' + str(k)
						spamwriter.writerow([vari] + [desc] + [code_correct[k-1]])
						vari = 'CKPT_' + str(k) + '_AnswerGiven'
						desc = 'Answer Selected at Checkpoint ' + str(k)
						spamwriter.writerow([vari] + [desc] + [code_given[k-1]])
						vari = 'CKPT_' + str(k) + '_Score'
						desc = 'Score (1 = Correct; 0 = Incorrect)'
						spamwriter.writerow([vari] + [desc] + [test_result[k-1]])
						vari = 'CKPT_' + str(k) + '_Confidence'
						desc = 'Confidence indicated at checkpoint'
						spamwriter.writerow([vari] + [desc] + [confidence_given[k-1]])
						k += 1
					spamwriter.writerow(['CKPT_NumComplete'] + ['Total Number of Checkpoints Completed (able to enter code)'] + [checkpoints_reached])
					spamwriter.writerow(['CKPT_TotalCorrect'] + ['Total Number of Checkpoints Correct'] + [checkpoints_correct])
					spamwriter.writerow(['Maximum HR'] + ['Maximum HR (entered at start screen)'] + [max_hr])

					i = 1
					while (i < 21):
						vari = 'HR_' + str(i)
						desc = 'Raw HR at timepoint ' + str(i)
						spamwriter.writerow([vari] + [desc] + ['NaN'])
						i += 1
					i = 1
					while (i < 21):
						vari = 'HR_Perc_' + str(i)
						desc = 'HR Percentage of Max at timepoint ' + str(i)
						spamwriter.writerow([vari] + [desc] + ['NaN'])
						i += 1
				successfully_formatted.append(raw_files)
				
			except:
				unable_to_format.append(raw_files)
		else:
			no_data_found.append(raw_files)

completed_files = []
total_completed_files = 0
arr = os.listdir()

for fileNames in arr:
	if fileNames.endswith(".csv"):
		if fileNames.startswith('NAVIGATE_'):
			completed_files.append(fileNames)
			total_completed_files += 1

with open('Aggregated_Data.csv', 'w', newline='') as outputFile:
	spamwriter = csv.writer(outputFile, delimiter=',', quotechar='|')
	spamwriter.writerow(['PID'] + ['Date'] + ['Start Time'] + ['Session'] + ['Condition'] + ['Map'] + ['Session Time'] + 
		['RPE_1'] + ['RPE_2'] + ['RPE_3'] + ['RPE_4'] + ['RPE_5'] + ['RPE_6'] + ['RPE_7'] + ['RPE_8'] + ['RPE_9'] + ['RPE_10'] +
		['JS_1'] + ['JS_2'] + ['JS_3'] + ['JS_4'] + ['JS_5'] + ['JS_6'] + ['JS_7'] + ['JS_8'] + ['JS_9'] + ['JS_10'] + 
		['CKPT_1_CorrectAnswer'] + ['CKPT_1_AnswerGiven'] + ['CKPT_1_Score'] + ['CKPT_1_Confidence'] + ['CKPT_2_CorrectAnswer'] + ['CKPT_2_AnswerGiven'] + ['CKPT_2_Score'] + ['CKPT_2_Confidence'] + 
		['CKPT_3_CorrectAnswer'] + ['CKPT_3_AnswerGiven'] + ['CKPT_3_Score'] + ['CKPT_3_Confidence'] + ['CKPT_4_CorrectAnswer'] + ['CKPT_4_AnswerGiven'] + ['CKPT_4_Score'] + ['CKPT_4_Confidence'] + 
		['CKPT_5_CorrectAnswer'] + ['CKPT_5_AnswerGiven'] + ['CKPT_5_Score'] + ['CKPT_5_Confidence'] + ['CKPT_6_CorrectAnswer'] + ['CKPT_6_AnswerGiven'] + ['CKPT_6_Score'] + ['CKPT_6_Confidence'] + 
		['CKPT_7_CorrectAnswer'] + ['CKPT_7_AnswerGiven'] + ['CKPT_7_Score'] + ['CKPT_7_Confidence'] + ['CKPT_8_CorrectAnswer'] + ['CKPT_8_AnswerGiven'] + ['CKPT_8_Score'] + ['CKPT_8_Confidence'] + 
		['CKPT_9_CorrectAnswer'] + ['CKPT_9_AnswerGiven'] + ['CKPT_9_Score'] + ['CKPT_9_Confidence'] + ['CKPT_10_CorrectAnswer'] + ['CKPT_10_AnswerGiven'] + ['CKPT_10_Score'] + ['CKPT_10_Confidence'] + 
		['CKPT_NumComplete'] + ['CKPT_TotalCorrect'] + ['Maximum HR'] +
		['HR_1'] + ['HR_2'] + ['HR_3'] + ['HR_4'] + ['HR_5'] + ['HR_6'] + ['HR_7'] + ['HR_8'] + ['HR_9'] + ['HR_10'] + 
		['HR_11'] + ['HR_12'] + ['HR_13'] + ['HR_14'] + ['HR_15'] + ['HR_16'] + ['HR_17'] + ['HR_18'] + ['HR_19'] + ['HR_20'] + 
		['HR_Perc_1'] + ['HR_Perc_2'] + ['HR_Perc_3'] + ['HR_Perc_4'] + ['HR_Perc_5'] + ['HR_Perc_6'] + ['HR_Perc_7'] + ['HR_Perc_8'] + ['HR_Perc_9'] + ['HR_Perc_10'] + 
		['HR_Perc_11'] + ['HR_Perc_12'] + ['HR_Perc_13'] + ['HR_Perc_14'] + ['HR_Perc_15'] + ['HR_Perc_16'] + ['HR_Perc_17'] + ['HR_Perc_18'] + ['HR_Perc_19'] + ['HR_Perc_20'])
	for finished_files in completed_files:
		file_data = []
		with open(finished_files, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			# Read through file to make sure there's more than one line of info
			first = True
			for row in spamreader:
				if first:
					nothing = 0
					first = False
				else:
					file_data.append(row[2])
		spamwriter.writerow(file_data)

if len(no_data_found) > 0:
	print('\nNo data found in: ', len(no_data_found))
	counter = len(no_data_found)
	while counter > 0:
		print(no_data_found[counter - 1])
		counter -= 1

if len(unable_to_format) > 0:
	print('\nOutdated format or unformattable raw data: ', len(unable_to_format))
	counter = len(unable_to_format)
	while counter > 0:
		print(unable_to_format[counter - 1])
		counter -= 1

if len(successfully_formatted) > 0:
	print('\nSuccessfully formatted: ', len(successfully_formatted))
	counter = len(successfully_formatted)
	while counter > 0:
		print(successfully_formatted[counter - 1])
		counter -= 1

print('\n')
