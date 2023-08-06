#!/bin/env python3
# coding:utf-8
"""
    配置主机组的联系人信息，更新到主机组内主机的inventory
"""
import json
import argparse
from zabbix_api import ZabbixAPI

def main():
    """
    读取 Contacts.json 文件中 HostGroup 联系人信息, 按 GroupName 升序排列
    遍历 HostGroup 并将 zabbix 中对应的 Host 更新 Poc 信息。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', required=True, help='URL of zabbix server')
    parser.add_argument('-u', '--user', required=True, help='Zabbix server login username')
    parser.add_argument('-p', '--password', required=True, help='Zabbix server login password')
    parser.add_argument('-c', '--contacts-file', required=True, help='HostGroup contacts file')
 
    args = parser.parse_args()
    contacts_file = args.contacts_file
    contacts = {}

    # 读取文件中 HostGroup 联系人信息, 生成contacts, [{group1's info}, {group2's info}, ...]
    with open(contacts_file, 'r', encoding='utf8')as fp:
        temp = json.load(fp)
        for info in temp['HostGroup']:
            contacts[info['GroupName']] = info

    # 登录zabbix
    zapi = ZabbixAPI(args.server, timeout=60)
    zapi.validate_certs = False
    zapi.login(args.user, args.password)

    zbx_groups = zapi.hostgroup.get({
        'output': ['groupid', 'name'],
        'selectHosts': ['hostid'],
        'filter': {'name': list(contacts.keys())}
    })
    
    # 将zbx_groups 按照 group name 升序排列
    zbx_groups.sort(key=lambda g: g.get('name'))

    for zbx_group in zbx_groups:
        # 获取 zbx_group 对应的 POC 信息
        contact = contacts.get(zbx_group.get('name'), {})

        zapi.host.massupdate({
            'hosts': zbx_group.get('hosts'),
            'inventory_mode': 1, # 1 - Automatic
            'inventory': {
                'poc_1_name': contact.get('poc_1_name'),
                'poc_1_email': contact.get('poc_1_email'),
                'poc_1_phone_a': contact.get('poc_1_phone_a'),
                'poc_1_phone_b': contact.get('poc_1_phone_b'),
                'poc_1_cell': contact.get('poc_1_cell'),
                'poc_1_screen': contact.get('poc_1_screen'),
                'poc_1_notes': contact.get('poc_1_notes'),
                'poc_2_name': contact.get('poc_2_name'),
                'poc_2_email': contact.get('poc_2_email'),
                'poc_2_phone_a': contact.get('poc_2_phone_a'),
                'poc_2_phone_b': contact.get('poc_2_phone_b'),
                'poc_2_cell': contact.get('poc_2_cell'),
                'poc_2_screen': contact.get('poc_2_screen'),
                'poc_2_notes': contact.get('poc_2_notes'),
            }
        })
        print(f"update success! HostGroup-> [{zbx_group.get('name')!r}] ")

    zapi.logout()


if __name__ == '__main__':
    main()

