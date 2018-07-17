import os
import time

from socket import *

if __name__ == "__main__":
    os.system('sudo killall udhcpd')
    print("1")
    os.system('sudo wpa_cli -i wlan0 terminate -B')
    print("2")
    time.sleep(1)
    os.system('echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward')
    os.system('sudo wpa_supplicant -d -Dnl80211 -c /etc/wpa_supplicant/wpa_supplicant.conf -iwlan0 -B')
    print("3")
    os.system('sudo wpa_cli -iwlan0 p2p_group_add')
    print("4")
    os.system('sudo ifconfig p2p-wlan0-0 192.168.1.2')
    print("5")
    os.system('sudo wpa_cli -i p2p-dev-wlan0 p2p_find')
    print("6")
    os.system('sudo wpa_cli -i p2p-dev-wlan0 p2p_peers')
    print("7")
    os.system('sudo wpa_cli -i p2p-dev-wlan0 wps_pbc')
    print("8")
    os.system('sudo udhcpd /etc/udhcpd.conf &')
   
 
    
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('', 6278))
    server.listen(1)
    print('listen...')
    client, addrClient = server.accept()
    print('connected to ',  )

    
    msg = client.recv(1024)
    while not msg or msg.__eq__('bye'):
        msg = str(msg).split("b'", 1)[1].rsplit("'",1)[0]
        #msg = str(msg).decode("utf-8", "ignore")
        print(msg)
        msg = client.recv(1024)

    
    client.close()
    server.close()
