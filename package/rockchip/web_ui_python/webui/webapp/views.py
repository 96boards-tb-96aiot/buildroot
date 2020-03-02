# -*- coding=utf-8 -*-
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from .models import *
from toybrick.toybrick import *
from toybrick.settings import *
from .factoryTest.factoryTest import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
# Create your views here.

@login_required
def index(request):
    # cpu information
    cpufreq_value = cpufreq()
    cpuload_value = cpuload()
    npufreq_value = npufreq()
    # ddr information
    ddrload_value = ddrload()
    ddrused_value = ddrused()
    ddrcap_value = ddrcap()
    # emmc information
    emmcload_value = emmcload()
    emmccap_value = emmccap()
    emmcused_value = emmcused()
    # temperature information
    tempload_value = tempload()
    currtemp_value = currtemp()
    criticaltemp_value = criticaltemp()
    # manufactureid = getmanufactureid()
    manufactureid, mac = get_mac_sn()
    mymode = getworkmode()
    usb_info = get_checked_usbfunction()
    rknn_info = getRKNN_Version()
    base_version = get_base_version()
    ip = get_stick_ip()
    port = get_stick_port()
    gateway = get_stick_gateway()
    dns1,dns2 = get_stick_dns_list()
    return render(request,'webapp/index.html',{'cpufreq':cpufreq_value,
                                               'cpuload':cpuload_value,
                                               'npufreq':npufreq_value,
                                               'ddrload':ddrload_value,
                                               'ddrused':ddrused_value,
                                               'ddrcap':ddrcap_value,
                                               'emmcload':emmcload_value,
                                               'emmccap':emmccap_value,
                                               'emmcused':emmcused_value,
                                               'tempload':tempload_value,
                                               'currtemp':currtemp_value,
                                               'criticaltemp':criticaltemp_value,
                                               'usb_info':usb_info,
                                               'rknn_info':rknn_info,
                                               'base_version':base_version,
                                               'manufactureid':manufactureid,
                                               'mac':mac,
                                               'mymode':mymode,
                                               'ip':ip,
                                               'port':port,
                                               'gateway':gateway,
                                               'dns1':dns1,
                                               'dns2':dns2})
@login_required
def workmode(request):
    mymode = getworkmode()
    return render(request,'webapp/workmode.html',{'mymode':mymode})

@login_required
def setmode(request):
    mymode = request.POST['select']
    res = setworkmode(mymode)
    if mymode == 'master':
        old_info = get_checked_usbfunction()
        new_info = old_info.replace("ntb,",'').replace("ntb",'')
        new_info_list = new_info.split(',')
        update_usb_info(new_info_list)
    if mymode == 'slave':
        old_info = get_checked_usbfunction()
        new_info = old_info.replace("ntb,",'').replace("ntb",'') + ",ntb"
        new_info_list = new_info.split(',')
        update_usb_info(new_info_list)
    if res == 0:
        flash = "update mode successfully,please reboot !"
        flag = 'text-info'
        return render(request,'webapp/workmode.html',{'mymode':mymode,"flash":flash,'flag':flag})
    else:
        return HttpResponse("set workmode error")

@login_required
def usbfunction(request):
    flash = ""
    flag = ''
    mymode = getworkmode()
    if request.method == 'POST':
        new_info = request.POST.getlist('usb')
        #html无法传值disable box，规避
        new_info = ['rndis','mass'] + new_info
        if mymode == 'slave':
            new_info = new_info + ['ntb']
        update_usb_info(new_info)
        flash = "update usbfunction successfully"
        flag = 'text-info'
    usb_info_all = get_all_usbfunction()
    usb_info_checked = get_checked_usbfunction()
    usb_list = usb_info_all.split(',')
    checked_list = usb_info_checked.split(',')
    workmode = getworkmode()
    return render(request,'webapp/usbfunction.html',{'usb_list':usb_list,"checked_list":checked_list,'flash':flash,'flag':flag,'workmode':workmode.strip()})

@login_required
def rpm(request):
    return render(request,'webapp/rpm.html')

@login_required
def pypackages(request):
    return render(request,'webapp/pypackages.html')

@login_required
def aiapp(request):
    return render(request,'webapp/aiapp.html')

@login_required
def password_setting(request):
    if request.method == 'POST':
        user = authenticate(username=request.user.username,password=request.POST['old'])
        if request.POST['new'] == request.POST['cnew'] and user !=None:
            flash = "update password successfully"
            flag = 'text-info'
            try:
                request.user.set_password(request.POST['new'])
                request.user.save()
                set_user_password(request.POST['new'])
            except:
                flash = "update password failed"
                flag = "text-danger"
        else:
            flash = "update password failed"
            flag = "text-danger"
        return render(request,'webapp/password_setting.html',{'flash':flash,'flag':flag})
    return render(request,'webapp/password_setting.html')

@login_required
def network(request):
    ip = get_stick_ip()
    dhcp_switch = get_dhcp_status()
    gateway = get_stick_gateway()
    dns1,dns2 = get_stick_dns_list()
    ip = get_stick_ip()
    webip = get_web_ip()
    return render(request,'webapp/network.html',{'ip':ip,'gateway':gateway,'dns1':dns1,'dns2':dns2,'webip':webip})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user=User.objects.create_user(username=username,password=password)
        if user:
            user = authenticate(username=username,password=password)
            login(request,user)
            return HttpResponse("注册成功")
        else:
            return HttpResponse("注册失败")

    else:
        return render(request,'webapp/register.html')
        # return render(request,'factoryApp/test.html',{'ip':ip})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        for key in request.POST:
            print key
        '''
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username =loginform.cleaned_data['username']
            password =loginform.cleaned_data['password']
        '''
        username =request.POST['uname']
        password =request.POST['psw']
        user = authenticate(username=username,password=password)
        print 'user:',user
        if user:
            login(request,user)
            user.last_seen = timezone.now()
            user.save()
            if user.isbackup == "no":
                toybrick_backup_config()
                user.isbackup = "yes"
                user.save()
            return redirect(reverse('webapp:index'))
        error_mesg = "Error! Invalid username or password, try again"
        return render(request,'webapp/login.html',{'error_mesg':error_mesg})
    else:
        return render(request,'webapp/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:index'))

@login_required
def isreboot(request):
    return render(request,'webapp/isreboot.html')

@login_required
def reboot(request):
    stickreboot()
    return redirect(reverse('webapp:index'))

def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True 
    else:
        return False

def network_setting(request,status):
    dhcp_switch = get_dhcp_status()
    port = get_stick_port()
    flash = ''
    flag = ''
    if request.method == 'POST':
        print request.POST
        dhcp = request.POST.get('dhcp')
        if dhcp is None:
            dhcp = "off"
        else:
            dhcp = "on"
        if dhcp == "off" and dhcp_switch == "off":
            ip = request.POST.get('ip')
            gateway = request.POST.get('gateway')
            dns1 = request.POST.get('dns1','')
            dns2 = request.POST.get('dns2','')
            if check_ip(ip.replace('/24','')) == False:
                flash = "ip addrss is illegal !"
                flag = "text-danger"
            if check_ip(dns1) == False and dns1 != '':
                flash = "DNS1 format is illegal !"
                flag = "text-danger"
            if check_ip(dns2) == False and dns2 != '':
                flash = "DNS2 format is illegal !"
                flag = "text-danger"
            if check_ip(gateway) == False:
                flash = "gateway format is illegal !"
                flag = "text-danger"
            if flash == '':
                update_stick_network(ip,gateway,dns1,dns2)
                set_dhcp_status(dhcp)
                flash = "update Network information successfully"
                flag = 'text-info'
        else:
            set_dhcp_status(dhcp)
            flash = "update Network information successfully"
            flag = 'text-info'
        # try:
            # port_val = int(port)
            # if port_val <= 0 or port_val >= 65535:
                # flash = "port is out of range !"
                # flag = "text-danger"
        # except:
            # flash = "port is out of range !"
            # flag = "text-danger"
    if status == '-1':
        flash = "dhcp set failed !"
        flag = "text-danger"
    elif status == '0':
        flash = "dhcp set successfully"
        flag = 'text-info'
    ip = get_stick_ip()
    dhcp_switch = get_dhcp_status()
    gateway = get_stick_gateway()
    dns1,dns2 = get_stick_dns_list()
    return render(request,'webapp/network_setting.html',{'ip':ip,'port':port,'gateway':gateway,'dns1':dns1,'dns2':dns2,'flash':flash,'flag':flag,'dhcp_switch':dhcp_switch})

def dhcp_setting(request):
    if request.POST.get("dhcp") is not None:
        dhcp = "on"
        print request.POST.get("dhcp")
        ret = set_dhcp_status(dhcp)
    return redirect(reverse('webapp:network_setting',args=(ret,)))

def reboot_ajax(request):
    flag = request.GET.get('flag')
    if flag == "reboot":
        stickreboot()
    res = {}
    res['ans'] = 'ok'
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def help(request):
    webip = get_dhcp_ip()
    # port = get_stick_port()
    port = "80"
    ip = "http://" + webip.replace('/24','')
    if port != '80':
        ip = ip + ':' + port
    return render(request,'webapp/help.html',{'ip':ip})

def isupdate(request):
    return render(request,'webapp/isupdate.html')

def update_ajax(request):
    result = stick_update()
    res = {}
    res['ans'] = result
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def install_ajax(request):
    pkgname = request.GET.get('pkgname')
    result = rpmpackage_install(pkgname)
    res = {}
    res['ans'] = result
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def restore_factory_settings(request):
    user = User.objects.get(username=DEFAULT_USER)
    user.set_password(DEFAULT_PSW)
    user.save()
    set_user_password(DEFAULT_PSW)
    toybrick_restore_factory_conf()
    return redirect(reverse('webapp:index'))
#factory test
#############################################

def fttest(request):
    factorydata = FactoryData.objects.all()
    if list(factorydata) == []:
        factorydata = FactoryData()
        factorydata.save()
    else:
        factorydata = factorydata[0]
    manufactureid = getmanufactureid()
    return render(request,'webapp/factorytest.html',{'factorydata':factorydata, 'manufactureid':manufactureid,})

def isrecovery(request):
    manufactureid = getmanufactureid()
    return render(request,'webapp/isrecovery.html',{'manufactureid':manufactureid,})

def recovery(request):
    res = stick_recovery()
    if res == 0:
        result = "恢复出厂设置成功"
    else:
        result = "恢复出厂设置失败"
    manufactureid = getmanufactureid()
    return render(request,'webapp/recovery_result.html',{'result':result, 'manufactureid':manufactureid,})

def stress_test(request):
    # factorydata = FactoryData.objects.all()
    # if list(factorydata) == []:
        # factorydata = FactoryData()
        # factorydata.save()
    # else:
        # factorydata = factorydata[0]
    stressresult = stress('')
    manufactureid = getmanufactureid()
    return render(request,'webapp/stress_test.html',{'stressresult':stressresult, 'manufactureid':manufactureid,})

def test_ajax(request):
    item = request.GET.get('item')
    result = factorytest(item)
    save_test_result(item,result)
    res = {}
    res['ans'] = result
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def stress_ajax(request):
    item = request.GET.get('item')
    testtime = request.GET.get('testtime')
    result = stress(testtime)
    save_test_result(item,result)
    res = {}
    res['ans'] = result
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def page_ajax(request):
    item = request.GET.get('item')
    res = {}
    res['ans'] = item
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def read_ajax(request):
    item = request.GET.get('item')
    res = {}
    factorydata = FactoryData.objects.all()
    if list(factorydata) == []:
        factorydata = FactoryData()
        factorydata.save()
    else:
        factorydata = factorydata[0]
    if item == "nresult":
        res['ans'] = factorydata.npuresult
    elif item == "uresult":
        res['ans'] = factorydata.usbresult
    elif item == "dresult":
        res['ans'] = factorydata.ddrresult
    elif item == "sresult":
        res['ans'] = factorydata.stressresult
    if res['ans'] == 'None':
        res['ans'] = stress('')
    j_ret = json.dumps(res)
    return HttpResponse(j_ret)

def save_test_result(item,result):
    factorydata = FactoryData.objects.all()
    if list(factorydata) == []:
        factorydata = FactoryData()
        factorydata.save()
    else:
        factorydata = factorydata[0]
    if item == "nresult":
        factorydata.npuresult = result
    elif item == "uresult":
        factorydata.usbresult = result
    elif item == "dresult":
        factorydata.ddrresult = result
    elif item == "sresult":
        #压力测试结果不放入数据库
        factorydata.stressresult = "None"
    factorydata.save()

#############################################
