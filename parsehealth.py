#!/usr/bin/python
#Simple Python script to parse Apple Health Values out of the export.xml into a pipe delimited txt file

import re, sys, os

# Assumes you run the script in same location as the exported data
healthlog = open("export.xml","r")

# Open Parsed results file
healthresults = open("AppleHealthData.txt","w")

#Create Header row 
healthresults.write("DateTime|Source|HealthType|HealthValue\n")

# Initi counter
count =0

#Init Health type value dictionary

valdic ={}
sourcedic ={}

#determine number of lines in export.xml
num_lines = sum(1 for line in open("export.xml"))


# loop through export.eml
for line in healthlog:
	#find record types
	if re.search(r"<Record type=", line):
		recordtype = re.search(r"<Record type=\"\S+\"",line)
		recordtypeval = recordtype.group()

		# Add record types to value dictionary
		valdic[recordtypeval[15:-1]] = count

		# get source of value			
		sourceName =re.search(r"sourceName\S\S\S+\s+\S+",line)
                sourceNameval = sourceName.group()
		sourcedic [sourceNameval[12:]] = count

		# Get value of record type 
		healthdata = re.search(r"value\S\S\w+",line)
                if healthdata is None:
			healthdata = "No Val"
		else: 
			healthdataval = healthdata.group()

		#Get end date/time of data collection 
		datetime2 = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
		datetime2val = datetime2.group()

		# Output results to file
		healthresults.write(str(datetime2val[9:] + "|" + sourceNameval[12:] + "|" + recordtypeval[15:-1] + "|" + healthdataval[7:] +" \n"))
		count = count +1


		# print progress hash
		if count % 10000 == 0:
			print '{counts} of {nums}'.format(counts=count, nums=num_lines)
			sys.stdout.flush()

#Close files
healthlog.close()
healthresults.close()

#Print values parsed
print "Health Values Captured"
for key in valdic:
	print key
print "Device Sources of Health Data"
for key in sourcedic:
	print key


