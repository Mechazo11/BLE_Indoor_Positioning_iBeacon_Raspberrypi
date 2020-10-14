import blescan
import sys
import time
import math
import bluetooth._bluetooth as bluez
import numpy as np
from csv import writer

file_name = "data_sc1.csv"

# Global variable declaration
dev_id = 0
rssi_node = [0,0,0,0] # RSSI data for node B1, B2 and B3 respectively
ls = [""] # This value will hold the string output for each of the beacon located
minor = 0
rssi = 0
count = 0
cnt = []

try:
	sock = bluez.hci_open_dev(dev_id)
	print ("ble thread started")

except:
	print ("error accessing bluetooth device...")
    	sys.exit(1)
    
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

def get_rssi(beacon_list):
	ls = beacon_list.split (",")
	ls1 =[]
	ls1 = [ls[3], ls[5]]
	#print(ls1)

	# This part will be useful later on to figure out the master delay time
	ls2 = []
	for i1 in ls1:
		ls2.append(int(i1))
	#print(ls2)

	# Minor and rssi has to be updated for each string read
	beacon_minor = ls2[0]
	beacon_rssi = ls2[1]
	#print minor, rssi
	return beacon_minor,beacon_rssi

def write_to_csv(f_name, data):
    with open(f_name, 'a+') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(data)

while True:
    str = blescan.parse_events(sock, 10)
    print "----------"
    count = count + 1
    print("Loop count: {}".format(count))
    # Here we get all the necessary data
    for beacon in str:
        minor, rssi = get_rssi(beacon)
        #print("Minor = {0}, RSSI = {1}".format(minor, rssi)) # Debug
        
        if (minor == 1000):
            rssi_node[0] = rssi
        elif (minor == 2000):
            rssi_node[1] = rssi
        elif (minor == 3000):
            rssi_node[2] = rssi
        elif (minor == 4000):
            rssi_node[3] = rssi
    
    print "----------"
    print(rssi_node)
    write_to_csv(file_name,rssi_node)
    time.sleep(1) # This delay does not matter
# End of script
