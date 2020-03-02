# -*- coding=utf-8 -*-
import os

configfile = '/var/webui/conf/toybrick.conf'
base_version_file = '/etc/rootfsBaseversion'
# cpu information
def cpufreq():
    cmd = 'cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'
    fd = os.popen(cmd)
    line = fd.read()
    if line == '':
        line = '0'
    fd.close()
    freq = float(line.strip())/1000000
    return str(format(freq,'.2f')) + 'GHz'

def npufreq():
    try:
        cmd = 'cat /sys/kernel/debug/clk/clk_summary|grep "aclk_npu" '
        fd = os.popen(cmd)
        line = fd.read().split()[3]
        if line == '':
            line = '0'
        fd.close()
        freq = float(line.strip())/1000000000
    except:
        freq = 0
    return str(format(freq,'.2f')) + 'GHz'

def cpuload():
    cmd = "top -bn 1 | awk 'NR==2{print $8}'"
    fd = os.popen(cmd)
    line = fd.read()
    if line == '':
        line = '0'
    fd.close()
    res = 100 - float(line.replace("%", ""))
    return res

# ddr information
def ddrload():
    used = ddrused()
    total = ddrcap()
    load = float(used.replace('MB',''))/(float(total.replace('MB','')))
    return str(format(load*100,'.2f'))

def ddrused():
    cmd = "top -bn 1 | awk 'NR==1{print $2}'"
    fd = os.popen(cmd)
    total = fd.read()
    fd.close()
    used = format(float(total.replace('K',''))/(1024.0),'.2f')
    return str(used) + 'MB'

def ddrcap():
    cmd = "top -bn 1 | awk 'NR==1{print $4}'"
    fd = os.popen(cmd)
    total = fd.read()
    fd.close()

    cmd2 = "top -bn 1 | awk 'NR==1{print $2}'"
    fd2 = os.popen(cmd2)
    total2 = fd2.read()
    fd2.close()

    total_res = format((float(total.replace("K", '')) + float(total2.replace("K", '')))/(1024.0),'.2f')
    return str(total_res) + "MB"

# emmc information
def emmcload():
    total = emmccap()
    used = emmcused()
    load = float(used.replace('MB', ''))/float(total.replace("MB",''))
    return str(format(load*100,'.2f'))

def emmccap():
    cmd = "df -h | grep  userdata | awk -F' ' '{print $2}'"
    fd = os.popen(cmd)
    total = fd.read()
    fd.close()
    total = total.replace('G','')
    total = float(total) * 1024
    return str(total)+'MB'

def emmcused():
    cmd = "df -h | grep userdata | awk -F' ' '{print $3}'"
    fd = os.popen(cmd)
    used = fd.read()
    fd.close()
    return used.replace('M','MB')

# temperature information
def tempload():
    current = currtemp()
    critical = criticaltemp()
    load = float(current)/float(critical)
    return str(format(load*100,'.2f'))

def currtemp():
    cmd = "cat /sys/class/thermal/thermal_zone0/temp"
    fd = os.popen(cmd)
    temp = fd.read()
    if temp == "":
        temp = '0'
    fd.close()
    
    temp = str(format(float(temp)/1000,'.2f'))
    return temp

def criticaltemp():
    cmd = "cat /sys/class/thermal/thermal_zone0/trip_point_1_temp"
    fd = os.popen(cmd)
    temp = fd.read()
    if temp == "":
        temp = '0'
    fd.close()
    temp = str(format(float(temp)/1000,'.2f'))
    return temp

def getmanufactureid():
    cmd = "sudo rockchip_vendor get manufacture 17 | awk -F' ' '{print $3}'"
    fd = os.popen(cmd)
    temp = fd.read()
    fd.close()

    if temp == "":
        temp = "00000000000000000"

    return temp

def getworkmode():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('workmode') != -1:
            ans = line.replace('workmode = ','')
            return ans.strip()
    return 'Unknown'

def setworkmode(mode):
    new_list = []
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('workmode') != -1:
            newline = 'workmode = ' + mode + '\n'
        else:
            newline = line
        new_list.append(newline)
    with open(configfile,'w+') as fs:
        fs.writelines(new_list)
    return 0
def set_dhcp_status(status):
    new_list = []
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('dhcp') != -1:
            newline = 'dhcp = ' + status + '\n'
        else:
            newline = line
        new_list.append(newline)
    with open(configfile,'w+') as fs:
        fs.writelines(new_list)
    return 0
def stickreboot():
    cmd = "sudo reboot"
    res = os.system(cmd)
    return res

def set_user_password(password):
    print password
    return 0

def get_checked_usbfunction():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('usbfunc') != -1:
            ans = line.replace('usbfunc = ','')
            return ans.strip()
    return 'rndis,ntb,mass'

def get_all_usbfunction():
    # return 'rndis,ntb,mass,uart'
    return 'rndis,ntb,mass'

def getRKNN_Version():
    cmd = "rpm -qi rknn |grep 'Version'|awk '{print $3}'"
    fd = os.popen(cmd)
    version = fd.read().strip()
    if version == "":
        version = '0.0.0'
    return version

def get_base_version():
    base_version = "Not Found"
    #with open(base_version_file,'r+') as fd:
    #    base_version = fd.read()
    return base_version
def get_static_ip():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('web') == -1 and line.find('ip') != -1:
            ans = line.replace('ip = ','')
            return ans.strip()
    return ''

def get_stick_port():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('webport') != -1:
            ans = line.replace('webport = ','')
            return ans.strip()
    return ''

def get_static_gateway():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('web') == -1 and line.find('gateway') != -1:
            ans = line.replace('gateway = ','')
            return ans.strip()
    return ''

def get_static_dns_list():
    dns1 = ''
    dns2 = ''
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('DNS1') != -1:
            dns1 = line.replace('DNS1 = ','').strip()
        if line.find('#') == -1 and line.find('DNS2') != -1:
            dns2 = line.replace('DNS2 = ','').strip()
    return dns1,dns2

def update_stick_network(ip,gateway,dns1,dns2):
    new_list = []
    isfindip = False
    isfindgateway = False
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('web') == -1 and line.find('ip') != -1:
            newline = 'ip = ' + ip + '\n'
            isfindip = True
        elif line.find('#') == -1 and line.find('web') == -1 and line.find('gateway') != -1:
            newline = 'gateway = ' + gateway + '\n'
            isfindgateway = True
        elif line.find('#') == -1 and line.find('DNS1') != -1:
            newline = 'DNS1 = ' + dns1 + '\n'
        elif line.find('#') == -1 and line.find('DNS2') != -1:
            newline = 'DNS2 = ' + dns2 + '\n'
        else:
            newline = line
        new_list.append(newline)
    if isfindip == False:
        newline = 'ip = ' + ip + '\n'
        new_list.append(newline)
    if isfindgateway == False:
        newline = 'gateway = ' + gateway + '\n'
        new_list.append(newline)
    with open(configfile,'w+') as fs:
        fs.writelines(new_list)
    return 0

def update_usb_info(usb_info):
    new_info = ''
    for u in usb_info:
        if new_info == '':
            new_info = u
        else:
            if u != '':
                new_info = new_info + ',' + u
    new_list = []
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('usbfunc') != -1:
            newline = 'usbfunc = ' + new_info + '\n'
        else:
            newline = line
        new_list.append(newline)
    with open(configfile,'w+') as fs:
        fs.writelines(new_list)
    return 0

def dnf_cmd(cmd):

    os.system(cmd)

    fd = open("/var/log/webui.log", "r")
    line = fd.read()
    fd.close()
    if line.find("Complete") != -1:
        return 0
    else:
        return -1

def stick_update():
    cmd = "sudo dnf -y update > /var/log/webui.log"
    return dnf_cmd(cmd)

def rpmpackage_install(name):
    cmd = "sudo dnf -y install %s > /var/log/webui.log"%name
    return dnf_cmd(cmd)

def get_dhcp_status():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('dhcp') != -1:
            ans = line.replace('dhcp = ','')
            return ans.strip()
    return ''

def get_dhcp_ip():
    cmd = "ip a|grep eth0|grep inet|awk -F' ' '{print $2}'"
    fd = os.popen(cmd)
    line = fd.read()
    fd.close()
    res = line.strip()
    if line == '':
        res = get_web_ip()
    return res

def get_dhcp_gateway():
    cmd = "route -n|grep UG|awk -F' ' '{print $2}'"
    fd = os.popen(cmd)
    line = fd.read()
    fd.close()
    res = line.strip()
    if line == '':
        res = get_web_gateway()
    return res

def get_dhcp_dns_list():
    dns1 = ''
    dns2 = ''
    cmd = "cat /etc/resolv.conf|grep nameserver|grep -v run|awk -F' ' '{print $2}'"
    fd = os.popen(cmd)
    line = fd.read()
    fd.close()
    dns_list = line.strip().split('\n')
    if len(dns_list) >= 2:
        dns1 = dns_list[0]
        dns2 = dns_list[1]
    if len(dns_list) == 1:
        dns1 = dns_list[0]
    return dns1,dns2

def get_stick_ip():
    # dhcp_switch = get_dhcp_status()
    # if dhcp_switch == 'on':
    #     res = get_dhcp_ip()
    # else:
    #     res = get_static_ip()
    res = get_dhcp_ip()
    if res == "":
        res = get_web_ip()
    return res

def get_stick_gateway():
    # dhcp_switch = get_dhcp_status()
    # if dhcp_switch == 'on':
    #     res = get_dhcp_gateway()
    # else:
    #     res = get_static_gateway()
    res = get_dhcp_gateway()
    if res == "":
        res = get_web_gateway()
    return res

def get_stick_dns_list():
    # dhcp_switch = get_dhcp_status()
    # if dhcp_switch == 'on':
    #     res = get_dhcp_dns_list()
    # else:
    #     res = get_static_dns_list()
    res = get_dhcp_dns_list()
    return res

def get_web_ip():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('webip') != -1:
            ans = line.replace('webip = ','')
            return ans.strip()
    return ''

def get_web_gateway():
    with open(configfile,'r+') as fd:
        lines = fd.readlines()
    for line in lines:
        if line.find('#') == -1 and line.find('webgateway') != -1:
            ans = line.replace('webgateway = ','')
            return ans.strip()
    return ''

def toybrick_backup_config():
    cmd = "cp /var/webui/conf/toybrick.conf /var/webui/conf/toybrick.conf.backup"
    res = os.system(cmd)
    return res

def toybrick_restore_factory_conf():
    cmd = "cp /var/webui/conf/toybrick.conf.backup /var/webui/conf/toybrick.conf"
    res = os.system(cmd)
    return res

def getHwAddr(ifname):
    import socket, struct, fcntl
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


def get_mac_sn():
    sn = 'error'
    mac = 'error'
    try:
        result = os.popen('/usr/lib/webui/bin/vendor_test')
        res = result.read()
        for line in res.splitlines():
            if line.find('Sn') > -1:
                sn = line[line.find('Sn'):].split('=')[-1].strip()
    except:
        pass

    try:
        _mac = getHwAddr('eth0')
        mac = _mac.replace(':', '').upper()
    except:
        pass
    print "sn: ", sn, "mac: ", mac
    return sn, mac
