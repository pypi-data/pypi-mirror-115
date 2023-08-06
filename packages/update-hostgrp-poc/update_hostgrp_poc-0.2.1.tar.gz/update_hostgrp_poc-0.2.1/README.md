# hostgrp-poc

配置主机组的联系人信息，更新到主机组内主机的inventory

# 说明
* 主机组的联系人信息来源为 Contacts.json, 取主机组，按组名升序排序
* 通过[zabbix_api](https://www.zabbix.com/documentation/4.0/manual/api/reference/host/massupdate)调用 [host.massupdate](https://www.zabbix.com/documentation/4.0/manual/api/reference/host/massupdate) 方法更新此主机组内 Host 的inventory 中 POC 信息。
更新此主机组内主机的inventory信息


# 使用
* `python setup.py install`
* `update-hostgrp-poc -s http://10.190.5.44/zabbix -u liusong -p liusong602B`

```
usage: update-hostgrp-poc [-h] -s SERVER -u USER -p PASSWORD -c CONTACTS_FILE

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        URL of zabbix server
  -u USER, --user USER  Zabbix server login username
  -p PASSWORD, --password PASSWORD
                        Zabbix server login password
  -c CONTACTS_FILE, --contacts-file CONTACTS_FILE
                        HostGroup contacts file
```
contacts-file 文件请参考 src/Contacts.json。
