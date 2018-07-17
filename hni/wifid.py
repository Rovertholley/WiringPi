import os
import time


def setup_conf_files():
    dir = os.path.dirname(__file__) + '/conf/' 
    _copy_file_no_overwriting(os.path.abspath(dir + 'dhcpd.conf'), os.path.abspath('/etc/dhcp/dhcpd.conf'))
    _copy_file_no_overwriting(os.path.abspath(dir + 'udhcpd.conf'), os.path.abspath('/etc/udhcpd.conf'))
    _copy_file_no_overwriting(os.path.abspath(dir + 'wpa_supplicant.conf'), os.path.abspath('/etc/wpa_supplicant/wpa_suplicant.conf'))


def _copy_file_no_overwriting(src, dst):
    import shutil
    if not os.path.isfile(dst):
        print('copying... ', dst)
        shutil.copyfile(src, dst)



def _system_critical(command):
   if os.system(command) is not 0:
       raise ConnectionError('wifi direct failed ')


def start_as_go_fedora(str_interface='wls35u1', str_static_ip_addr_for_p2p='192.168.1.2'):
    os.system('sudo killall dhcpd')  # dhcpd
    os.system('sudo wpa_cli -i ' + str_interface + ' terminate -B')  
    # os.system('sudo wpa_cli -i p2p-' + str_interface + '-0 terminate -B')
    time.sleep(2) 
    os.system('echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward')  # ip
    # os.system('echo "ctrl_interface=/var/run/wpa_supplicant\nupdate_config=1" | sudo tee /etc/wpa_supplicant.conf')
    _system_critical('sudo wpa_supplicant -d -Dnl80211 -c /etc/wpa_supplicant.conf -i' + str_interface + ' -B')  # 
    _system_critical('sudo wpa_cli -i' + str_interface + ' p2p_group_add')
    # p2p_group_add: Become an autonomous GO (p2p )
    _system_critical('sudo ifconfig p2p-' + str_interface + '-0 ' + str_static_ip_addr_for_p2p)  # p2p 
    _system_critical('sudo wpa_cli -i p2p-' + str_interface + '-0 p2p_find')  # p2p_find: Enables discovery
    os.system('sudo wpa_cli -ip2p-' + str_interface + '-0 p2p_peers')
    # p2p_peers: Shows list of discovered peers (not necessary)
    _system_critical('sudo wpa_cli -ip2p-' + str_interface + '-0 wps_pbc')
    # wps_pbc: pushbutton for GO WPS authorization to accept incoming connections (When devices try to connect to GO)
    _system_critical('sudo dhcpd') 


def start_as_go_ubuntu(str_interface='wlan0', str_static_ip_addr_for_p2p='192.168.1.2'):
    os.system('sudo killall udhcpd')
    os.system('sudo wpa_cli -i ' + str_interface + ' terminate -B')
    print("1")
    # os.system('sudo wpa_cli -i p2p-' + str_interface + '-0 terminate -B')
    time.sleep(1)
    os.system('echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward')
    print("2")
    # os.system('echo "ctrl_interface=/var/run/wpa_supplicant\nupdate_config=1" | sudo tee /etc/wpa_supplicant.conf')
    _system_critical('sudo wpa_supplicant -d -Dnl80211 -c /etc/wpa_supplicant/wpa_supplicant.conf -i' + str_interface + ' -B')
    print("3")
    _system_critical('sudo wpa_cli -i' + str_interface + ' p2p_group_add')
    print("4")
    _system_critical('sudo ifconfig p2p-' + str_interface + '-0 ' + str_static_ip_addr_for_p2p)
    print("5")
    _system_critical('sudo wpa_cli -i p2p-' + str_interface + '-0 p2p_find')
    print("6")
    os.system('sudo wpa_cli -ip2p-' + str_interface + '-0 p2p_peers')
    print("7")
    _system_critical('sudo wpa_cli -ip2p-' + str_interface + '-0 wps_pbc')
    print("8")
    _system_critical('sudo udhcpd /etc/udhcpd.conf &')
    


if __name__ == "__main__":
# example
    try:
        start_as_go_ubuntu()
    except ConnectionError:
       print('ConnectionError from wifid')
