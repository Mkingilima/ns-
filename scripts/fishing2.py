import re
import csv

# Function to extract data from mylogs.txt
def extract_data(filename):
    sim_time = None
    dev_id = None
    packet = None
    snr = None
    rssi = None
    probability_of_success = None
    sf = None

    with open(filename, 'r') as file:
        for line in file:
            # Extract sim_time
            if 'Seconds:' in line:
                sim_time = float(re.findall(r'Seconds:\s+(\d+\.\d+)', line)[0])

            # Extract dev_id, packet, SNR, RSSI, probability_of_success, and SF
            if 'Rx packet:' in line:
                dev_id = int(re.findall(r'devId:(\d+)', line)[0])
                packet = int(re.findall(r'packet:(\d+)', line)[0])
                snr = float(re.findall(r'SNR:(-?\d+\.\d+)', line)[0])
                rssi = float(re.findall(r'RSSI:(-?\d+\.\d+)', line)[0])
                probability_of_success = float(re.findall(r'Probability:(\d+\.\d+)', line)[0])
                sf = int(re.findall(r'SF:(\d+)', line)[0])

                yield sim_time, dev_id, packet, snr, rssi, probability_of_success, sf

# Function to write data to CSV files
def write_to_csv(filename, data, headers):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

# Extract data from mylogs.txt
data = extract_data('mylogs.txt')

# Separate data for different types of logs
gw_packet_receive_data = []
dev_packet_receive_data = []
packet_tracking_data = []

for entry in data:
    sim_time, dev_id, packet, snr, rssi, probability_of_success, sf = entry

    if dev_id == 0:
        gw_packet_receive_data.append([sim_time, dev_id, packet, snr, rssi, probability_of_success, sf])
    else:
        dev_packet_receive_data.append([sim_time, dev_id, packet, snr, rssi, probability_of_success, sf])
    
    packet_tracking_data.append([sim_time, dev_id, packet, snr, rssi, probability_of_success, sf])

# Write data to CSV files
write_to_csv('result/gw_receiving_tracker.csv', gw_packet_receive_data, ['sim_time', 'dev_id', 'packet', 'SNR', 'RSSI', 'probability_of_success', 'SF'])
write_to_csv('result/device_sending_tracker.csv', dev_packet_receive_data, ['sim_time', 'dev_id', 'packet', 'SNR', 'RSSI', 'probability_of_success', 'SF'])
write_to_csv('result/packet_tracker.csv', packet_tracking_data, ['sim_time', 'dev_id', 'packet', 'SNR', 'RSSI', 'probability_of_success', 'SF'])
