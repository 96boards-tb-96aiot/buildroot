# -*- coding=utf-8 -*-
import time
import os

user = 'toybrick'
psw = 'toybrick'
escp = '/usr/bin/escp'
scp_source = '/rockchip_test/compute_stick_test/rknn_test/data/mobilenet_v1.rknn'
scp_source_tmp = '/home/toybrick/mobilenet_v1_tmp'
scp_dest = '%s@192.168.180.1:/home/%s/mobilenet_v1_tmp'%(user,user)
recovery_prog = '/usr/bin/recovery.sh'
# utest_size = '103M'
testtime_index = {
        '1':'1,1,1800',
        '60':'1,60,120000',
        '460':'1,450,900000',
        '690':'1,690,1380000',
        '1380':'1,1380,2760000',
}
stress_cfg = '/rockchip_test/compute_stick_test/.rk1808_test.cfg'
npu_result = '/rockchip_test/compute_stick_test/.npuresult.txt'
stress_result = '/rockchip_test/compute_stick_test/.stressresult.txt'
ddr_log = '/rockchip_test/compute_stick_test/.ddr_result.log'
# FactoryTest Function
def escp_cmd(cmd):
    os.system(cmd)
    fd = open("/var/log/factorytest.log", "r")
    line = fd.read()
    fd.close()
    if line.find("mobilenet_v1") != -1:
        return 0
    else:
        return -1
def npu():
    cmd = "sudo /usr/bin/ft_run.sh"
    res = os.system(cmd)
    return res

def usb():
    #记录MD5值
    time.sleep(20)
    #清除ssh
    clean_ssh = "sudo rm -rf /root/.ssh"
    os.system(clean_ssh)
    md5_cmd = "md5sum %s |awk '{print$1}'"%scp_source
    fd = os.popen(md5_cmd)
    md5_value_1 = fd.read()
    fd.close()
    #拷贝回宿主机
    scp_cmd = "%s %s %s %s > /var/log/factorytest.log"%(escp,psw,scp_source,scp_dest)
    res2 = escp_cmd(scp_cmd)
    #再次拷贝到计算棒，记录MD5值
    scp_cmd = "%s %s %s %s > /var/log/factorytest.log"%(escp,psw,scp_dest,scp_source_tmp)
    res3 = escp_cmd(scp_cmd)
    md5_cmd = "md5sum %s |awk '{print$1}'"%scp_source_tmp
    fd = os.popen(md5_cmd)
    md5_value_2 = fd.read()
    fd.close()
    if md5_value_1.strip() == md5_value_2.strip():
        res = 0 +res2 +res3
    else:
        res = -1
    clean_cmd = 'sudo rm -rf %s'%scp_source_tmp
    os.system(clean_cmd)
    clean_cmd = 'sudo rm -rf /var/log/factorytest.log'
    os.system(clean_cmd)
    return res

def ddr():
    logFile = ddr_log
    cmd = 'sudo /usr/bin/stressapptest -s 60 -i 4 -C 4 -W --stop_on_errors -M 128 >> '+ logFile + ' 2>&1'
    res = os.system(cmd)
    with open(logFile,'rb') as ff:
        for line in ff.readlines():
            if line.find('Status: PASS') >= 0:
                return 0
            else:
                pass
    return -1


def stress(testtime):
    res = 'None'
    if testtime != '':
        test_string = testtime_index[testtime]
        cmd = 'echo "%s" > %s '%(test_string,stress_cfg)
        res_write = os.system(cmd)
        sync_cmd = 'sync'
        res_sync = os.system(sync_cmd)
        if res_write != 0 or res_sync != 0:
            return 'fail'
        t = int(testtime)
        time.sleep(t*60+10)
    cmd1 = "sudo cat %s"%stress_result
    cmd2 = "sudo cat %s"%npu_result
    f1 = os.popen(cmd1)
    res1 = f1.read()
    f1.close()
    f2 = os.popen(cmd2)
    res2 = f2.read()
    f2.close()
    if res1.strip() != '' and res2.strip() != '':
        if res1.strip() == '0' and res2.strip() == '0':
            res = 'ok'
        else:
            res = 'fail'
    return res

def factorytest(item):
    test_list = {'nresult':npu,
                 'uresult':usb,
                 'dresult':ddr,
                 'sresult':stress,
                }
    func = test_list[item]
    res = func()
    if res == 0:
        res = 'ok'
    else:
        res = 'fail'
    return res

def stick_recovery():
    cmd = "sudo %s"%recovery_prog
    res =os.system(cmd)
    sync_cmd = 'sync'
    res_sync = os.system(sync_cmd)
    return res + res_sync
