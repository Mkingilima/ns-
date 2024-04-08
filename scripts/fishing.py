import re
import csv
import pandas as pd


def parse_logs():
    print('Reading packet trace')
    log_file = 'mylogs.txt'

    # Option 1: Exclude SNR/RSSI for Sent Packets (if not present in logs)
     regex_gw_receive = '([\d.]{1,})s (\d+) GatewayLorawanMac:Receive\(\):[\w :]+ ([0x\da-f]{5,}) SNR:(-?\d+.\d+) RSSI:(-?\d+.\d+)'
     regex_dev_send = '([\d.]{1,})s (\d+) TDMASender:ScheduleReach\(\):[\w :,-]+The packet: ([0x\da-f]{5,})'

    # Option 2: Capture SNR/RSSI for Both (if desired)
    #regex_gw_receive = '([\d.]{1,})s (\d+) GatewayLorawanMac:Receive\(\):[\w :,-]+ ([0x\da-f]{5,}) SNR:(-?\d+.\d+) RSSI:(-?\d+.\d+)'
    #regex_dev_send = '([\d.]{1,})s (\d+) TDMASender:ScheduleReach\(\):[\w :,-]+The packet: ([0x\da-f]{5,}) SNR:(-?\d+.\d+) RSSI:(-?\d+.\d+)'

    with open(log_time) as file:
        lines = file.readlines()
        dev_send_list = []
        gw_receive_list = []
        gw_fields = ['sim_time', 'dev_id', 'packet', 'SNR', 'RSSI']
        dev_fields = ['sim_time', 'dev_id', 'packet', 'SNR', 'RSSI']
        for line in lines:
            gw_res = re.search(regex_gw_receive, line)
            dev_res = re.search(regex_dev_send, line)
            if gw_res:
                rec = {}
                for idx, val in enumerate(gw_fields):
                    rec[gw_fields[idx]] = gw_res.group(idx + 1).strip()
                gw_receive_list.append(rec)
            if dev_res:
                rec = {}
                for idx, val in enumerate(dev_fields):
                    rec[dev_fields[idx]] = dev_res.group(idx + 1).strip()
                dev_send_list.append(rec)

        dev_file = 'result/device_sending_tracker.csv'
        gw_file = 'result/gw_receiving_tracker.csv'
        with open(dev_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=dev_fields)
            writer.writeheader()
            for data in dev_send_list:
                writer.writerow(data)

        with open(gw_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=gw_fields)
            writer.writeheader()
            for data in gw_receive_list:
                writer.writerow(data)

        combine_throughput(dev_file, gw_file)


def combine_throughput(dev_file, gw_file):
    with open(dev_file, 'r') as dev:
        dev_df = pd.read_csv(dev)
        dev_df.rename(columns={'sim_time': 'send_time'}, inplace=True)

    with open(gw_file, 'r') as gw:
        gw_df = pd.read_csv(gw)
        gw_df.rename(columns={'sim_time': 'recv_time'}, inplace=True)
        gw_df.rename(columns={'dev_id': 'gw_dev_id'}, inplace=True)

    gw_sub = gw_df[['recv_time', 'gw_dev_id', 'packet', 'SNR', 'RSSI']]
    df_O = pd.merge(dev_df, gw_sub, on="packet", how="left")
    df_O.to_csv("result/packet_tracker.csv", index=False, sep=',')  # Use ',' as delimiter


if __name__ == '__main__':
    parse_logs()
