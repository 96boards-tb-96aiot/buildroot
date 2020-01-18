#!/bin/sh
PATH=/bin:/sbin:/usr/bin:/usr/sbin
router_connted="no"
ping_period="4"
status_log="/tmp/wifi_status.log"

check_wlan=`ifconfig wlan0 2> /dev/null | grep  "Device not found"`
check_wpa=`wpa_cli -iwlan0 ping 2> /dev/null | grep PONG`

function main() {
    rm /tmp/setup_wifi_ok.log
    if [ $# -ge 2 ]; then
        echo -e "{ \042ssid\042: \042$1\042,\042psk\042: \042$2\042 }" > /tmp/connman_ap_ssid.json
    else
        usage
        exit 0
    fi

    ssid=$1
    password=$2
    if [ "`echo $password |wc -L`" -lt "8" ];then
        echo "waring: password lentgh is less than 8, it is not fit for WPA-PSK"
    fi

    setup_wifi

    if [ "${router_connted}" = "yes" ];then
        aplay /var/www/setup_wifi_ok.mp3
        echo "setup wifi success!!!"
        echo "ok" > /tmp/setup_wifi_ok.log
    else
        aplay /var/www/setup_wifi_error.mp3
        echo "setup wifi fail!!!"
        del_wifi
    fi
}

function usage() {
    echo "usage: $0  \"ssid\" \"key\""
}

function del_wifi() {
    wpa_cli -iwlan0 remove_network $id > /dev/null
    wpa_cli -iwlan0 save_config > /dev/null
}

function setup_wifi() {
    if [ -n "$check_wlan" ];then
        echo "wlan0 not set up, please check it!!!"
        exit 0
    fi
    if [ -z "$check_wpa" ];then
        echo "wpa_supplicant not set up, please check it!!!"
        exit 0
    fi

    id=`wpa_cli -iwlan0 add_network | grep -v "interface"`
    wpa_cli -iwlan0 set_network $id ssid \"${ssid}\" > /dev/null
    if [ "${password}" = "NONE" ]; then
        wpa_cli -iwlan0 set_network $id key_mgmt NONE > /dev/null
    else
        wpa_cli -iwlan0 set_network $id psk \"${password}\" > /dev/null
    fi
    wpa_cli -iwlan0 select_network $id  > /dev/null
    wpa_cli -iwlan0 enable_network $id  > /dev/null
    wpa_cli -iwlan0 save_config > /dev/null

    check_in_loop 50
    if [ $? -eq 0 ];then
        echo "ap connected success!!!"
        ping_test wlan0
    else
        echo "ap connected fail!!!"
    fi
}

function check_in_loop() {
    local cnt=1
    while [ $cnt -lt $1 ]; do
        local flag=1
        wpa_cli -iwlan0 status > ${status_log}
        while read line
        do
            local key=`echo $line | awk -F "=" '{print $1}'`
            local value=`echo $line | awk -F "=" '{print $2}'`
            if [[ "${key}" = "ssid" ]] && [[ "${value}" = "${ssid}" ]]; then
                flag=$((flag + 1))
            fi
            if [ "${key}" = "ip_address" ]; then
                flag=$((flag + 1))
                break;
            fi
        done < ${status_log} 
        if [ $flag -eq 3 ]; then
            return 0
        else
            cnt=$((cnt + 1))
            sleep 1
        fi
    done
    return 1
}

function ping_test() {
    router_ip=`dhcpcd -U $1 2> /dev/null | grep routers | awk -F "=" '{print $2}' | sed "s/'//g"`
    ping $router_ip -w $ping_period 
    if [ $? -eq 0 ];then
        echo "ping success!!!"
        router_connted="yes"
    else
        echo "ping fail, please check!!!"
    fi
}

main $@ > /tmp/web_setup_wifi.log
