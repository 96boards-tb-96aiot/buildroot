function handleCommand(command_xmlhttp, callback){
    if(command_xmlhttp.readyState==4){
        if(command_xmlhttp.status == 200){
            if(callback == null)
                return;
            callback(command_xmlhttp);
        }
    }
};

function send_commond(command, callback){
    var command_xmlhttp = GetXmlHttpObject();//create req obj
    command_xmlhttp.onreadystatechange = function () {//get data from web action
        handleCommand(command_xmlhttp, callback);
    }

    var url="cgi-bin/wifi/result.cgi?cmd=" + command;
    command_xmlhttp.open("GET", url , true);
    command_xmlhttp.setRequestHeader("If-Modified-Since", "0");
    command_xmlhttp.setRequestHeader("Cache-Control", "no-cache");
    command_xmlhttp.setRequestHeader("CONTENT-TYPE", "text/plain");
    command_xmlhttp.send(null);
 };

function get_wifi_list(){
    var wifi_json = send_commond("get_wifi_list", set_wifi_list_to_select);
};

function change_wifi_list(){
    document.getElementById("img1").src = "./images/refresh2.png";
    setTimeout(function(){
        document.getElementById("img1").src = "./images/refresh.png";
    },200);

    get_wifi_list();
};

function set_wifi(ssid,pwd){
    var wifi_ssid = ssid;
    var wifi_pwd = pwd;
    var wifi_json = send_commond("set_wifi&ssid=" + wifi_ssid + "&" + "pwd=" + wifi_pwd);
};

function set_wifi_list_to_select(command_xmlhttp){
    var response_data = command_xmlhttp.responseText;

    var obj_Data = eval("(" + response_data + ")");
    if(obj_Data.length > 10){
        var htmlNodes = '';

        for(var i = 0; i < obj_Data.length; i++){
            htmlNodes += '<a class="list-group-item" id="wifi_' + i + '"' + ' role="button" data-toggle="modal" data-target="#myModal">' + obj_Data[i].ssid + '</a>';
        }
        htmlNodes += '</ul>';

        $('#testtext').html(htmlNodes);

        var j;
        var index = 1;
        var wifi_select = document.getElementById("ssid");
        for(j = 0; j < obj_Data.length; j++){
            var wifi = new Object;
            wifi.ssid = obj_Data.aplist[j].ssid;
            wifi_select.Option.add(wifi.id);
        }
    }else
        get_wifi_list();
};

$('ul').on('click','a',function(){
    var inner_ssid = this.innerText;
    var my_ssid = document.getElementById("modal_ssid");
    var my_pwd = document.getElementById("modal_pwd");
    my_pwd.value = "";
    if (inner_ssid == "Setting Wifi Manually")
        my_ssid.value = "";
    else
        my_ssid.value = inner_ssid;
});

function set_wifi_by_modal_input(){
    setTimeout(function(){$("#mymodal").modal("hide")},2000);
    var input_ssid = document.getElementById("modal_ssid").value;
    var input_pwd = document.getElementById("modal_pwd").value;

    if (input_ssid != ""){
        set_wifi(input_ssid,input_pwd);
        setTimeout("location.href='./wait.html';", 0);
    }
};

function wait_result(){
    var wifi_json = send_commond("get_wifi_result&timeout=60", handle_result);
};

function handle_result(command_xmlhttp){
    if(command_xmlhttp.responseText == "error"){
        var text=document.getElementById("set_error");
        text.removeAttribute("hidden");
        setTimeout("location.href='./index.html';", 10000);
    }else if(command_xmlhttp.responseText == "ok"){
        var text=document.getElementById("set_ok");
        text.removeAttribute("hidden");
    }
};

