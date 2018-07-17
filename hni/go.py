import os

def _copy_file_no_overwriting(src, dst):
    import shutil
    if not os.path.isfile(dst):
        print('copying... ', dst)
        shutil.copyfile(src, dst)
        
dir = os.path.dirname(__file__)
_copy_file_no_overwriting(os.path.abspath(dir + '/dhcpd.conf'), os.path.abspath('/etc/dhcp/dhcpd.conf'))
_copy_file_no_overwriting(os.path.abspath(dir + '/udhcpd.conf'), os.path.abspath('/etc/udhcpd.conf'))
_copy_file_no_overwriting(os.path.abspath(dir + 'wpa_supplicant.conf'), os.path.abspath('/etc/wpa_supplicant/wpa_suplicant.conf'))
