from datetime import date #импорт модуля для определения текущей даты
import os #импорт модуля для работы с папками в оси, для создания папки
from typing import TextIO
#Функция возвращающая hostname коммутатора
def get_sysname(text):
    for line in text:
        if 'sysname' in line:
            return line.split()[1]

#Функция возвращающая все вланы используемые на коммутаторе
def get_vlans(text):
    vlans = list()
    for i in range(len(text)):
        if text[i].startswith('vlan') and text[i + 1].find('ACS') == -1:
                vlans.append(text[i].split()[1])
                vlans.append(text[i + 1].split()[1])
    return vlans

#Функция возвращаюзая ip адрес и маску коммутатора
def get_ip(text):
    for line in text:
        if 'ip address 10.' in line:
            return line.strip()

#Функция возвращаюзая шлюз
def get_gw(text):
    for line in text:
        if 'ip route-static' in line:
            return line.split()[4]

#Функция возвращающая описание портов
def get_description(text):
    descriptions = list()
    for i in range(len(text)):
        if text[i].startswith('interface Ethernet') or text[i].startswith('interface GigabitEthernet'):
            if text[i + 1].startswith(' description') == False:
                descriptions.append('!')
            else:
                descriptions.append(text[i + 1].strip().replace('"', '')[12:])
    return descriptions

#Функция возвращающая настройки для портов.
def get_port_status(text):
    port_status = [[], []]
    for i in range(len(text)):
        if text[i].startswith('interface Ethernet'):
            port_status[0].append(text[i].strip()[18:])
            if text[i + 1].startswith(' description') == False:
                i -= 1
            if text[i + 2].startswith(" shutdown"):
                port_status[1].append(text[i + 2].strip())
            elif text[i + 2].startswith(" port link-type access"):
                port_status[1].append(text[i + 3].strip())
            else:
                    if text[i + 3].startswith(' port trunk pvid') and text[i + 4].startswith(' port trunk allow-pass vlan'):
                        port_status[1].append(text[i + 3] + text[i + 4])
                    elif text[i + 3].startswith(' port trunk pvid') and text[i + 4].startswith(' undo port trunk allow-pass vlan'):
                        port_status[1].append(text[i + 3] + text[i + 5])
                    elif text[i + 3].startswith(' undo port trunk allow-pass vlan'):
                        port_status[1].append(text[i + 4])
                    elif text[i + 3].startswith(' port trunk allow-pass'):
                        port_status[1].append(text[i + 3])
                    else:
                        port_status[1].append("shutdown")
    return port_status

#Создаёи описани вланов
def get_vlans_names(ls):
    s = ''
    for i in range(1, len(ls), 2):
        if ls[i - 1] != iptv and ls[i - 1] != management:
            s += f'vlan {ls[i - 1]}\n  name {ls[i]}\n!\n'
    return s


old_conf = open('oldconfig.cfg', 'r', encoding='utf-8')
conf_text = old_conf.readlines()
sys_name = get_sysname(conf_text)
ip = get_ip(conf_text)
gw = get_gw(conf_text)
print(sys_name)
print(ip, gw)
description_list = get_description(conf_text)
vlans_list = get_vlans(conf_text)
management = ''.join([vlans_list[i - 1] for i in range(0, len(vlans_list)) if vlans_list[i] == "management" or vlans_list[i] == "managament" ]) #находим влан управления
print(management)
iptv = ''.join([vlans_list[i - 1] for i in range(0, len(vlans_list)) if vlans_list[i] == "IPTV"]) #находим iptv влан
vlans_names = get_vlans_names(vlans_list)
all_vlans = ",".join(vlans_list[0::2])
port_status = get_port_status(conf_text)
#заменяем статус портов на соответствующий для коммутатора eltex2424p
for i in range(len(port_status[1])):
    x = ''
    ls = []
    x = port_status[1][i]
    ls = x.split()
    s = ''
    if ls[0] == "shutdown":
        continue
    elif ls[1] == 'default':
        port_status[1][i] = f'switchport mode access\n  switchport access vlan {ls[3]}'
    elif ls[2] == 'pvid':
        s = ','.join(ls[9:])
        port_status[1][i] = f'switchport mode general\n  switchport general pvid {ls[4]}\n  switchport general allowed vlan {s}'
    elif ls[2] == 'allow-pass':
        s = ','.join(ls[4:])
        port_status[1][i] = f'switchport mode general\n  switchport general allowed vlan {s}'


print(vlans_list)
print(description_list)
date = 'backup/' + str(date.today())
empty_config = open('MES2424.txt', 'r', encoding='utf-8')
conf_text = empty_config.read()
new_text = conf_text.replace('<hostname>', sys_name)
new_text = new_text.replace('<ip>', ip)
new_text = new_text.replace('<gw>', gw)
new_text = new_text.replace('<management>', management)
new_text = new_text.replace('<iptv>', iptv)
new_text = new_text.replace('<vlans_names>', vlans_names.strip())
new_text = new_text.replace('<all_vlans>', all_vlans)
for el in range(0,len(description_list)):
    new_text = new_text.replace('<desc>', f'"{description_list[el]}"', 1)
for ports in range(len(port_status[1])):
    new_text = new_text.replace('<status>', port_status[1][ports], 1)
filename = 'startup.conf'
tftp = open('tftp.txt', 'r', encoding='utf-8')
#Берётся путь из файла tftp.txt для сохранения готовой конфигурации в папке по данному пути
tftp_wey = tftp.readlines()[0].strip()
tftp.close()
output = open(f'{tftp_wey}{filename}', 'w', encoding='utf-8')
print(new_text, file=output)
#Проверяем есть ли папка для бекапа на сегодняшнуюю дату, если нет создаём её
if os.path.exists(date) == False:
    os.mkdir(date)
output2 = open(f'{date}/{sys_name}.conf', 'w', encoding='utf-8')
print(new_text, file=output2)
empty_config.close()
output.close()

