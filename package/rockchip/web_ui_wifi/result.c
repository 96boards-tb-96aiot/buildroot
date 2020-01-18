#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(void){
    printf("Content-type:text/html\n\n");
    char *getstr;
    getstr = getenv("QUERY_STRING");
    if(getstr == NULL)
        printf("get parameter error\n");
    if(strstr(getstr, "cmd=get_wifi_list") != NULL){
        int size = 0;
        FILE *fp = NULL;
        char *buf = NULL;
        struct stat fileinfo;
        char filename[] = "/tmp/wifi_list.txt";

        system("./scan_list.sh");

        if(stat(filename, &fileinfo) == -1) return 0;
        size = fileinfo.st_size;
        buf = (char *) calloc(size + 1, sizeof(char));

        fp = fopen(filename, "r");
        if(fp == NULL) return 0;

        if(fgets(buf, size + 1, fp) == NULL){
            fclose(fp);
            return 0;
        }

        if(buf[size] == '\n'){
            buf[size] = '\0';
            size--;
        }
        printf("%s\n", buf);

        free(buf);
        fclose(fp);
    }else if(strstr(getstr, "cmd=set_wifi") != NULL){
        char ssid[64] = {0};
        char psk[514] = {0};
        char str[600] = {0};

        sscanf(getstr, "cmd=set_wifi&ssid=%s", str);
        int index = strstr(str, "&pwd=") - str;
        int end = strlen(str);
        strncpy(ssid, str, index);
        strncpy(psk, str + index + 5, end - index - 5);
        memset(str, 0, 600);

        sprintf(str, "./wifi_tool.sh \"%s\" \"%s\"", ssid, psk);
        system(str);
    }else if(strstr(getstr, "cmd=get_wifi_result") != NULL){
        int timeout = 0;
        sscanf(getstr, "cmd=get_wifi_result&timeout=%d", &timeout);
        int count = timeout/10;
        while(count > 0){
            if(access("/tmp/setup_wifi_ok.log", 0) == 0){
                printf("ok");
                return 0;
            }
            count--;
            sleep(10);
        }
        printf("error");
    }
    return 0;
}
