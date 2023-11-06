def get_sysname(text):
    for line in text:
        if 'sysname' in line:
            return line.split()[1]

def get_vlans(text):
    vlans = list()
    for i in range(len(text)):
        if text[i].startswith('vlan') and text[i + 1].find('ACS') == -1:
                vlans.append(text[i].split()[1])
                vlans.append(text[i + 1].split()[1])
    return vlans


def get_ip(text):
    for line in text:
        if 'ip address 10.' in line:
            return line.strip()


def get_gw(text):
    for line in text:
        if 'ip route-static' in line:
            return line.split()[4]


def get_description(text):
    descriptions = list()
    for i in range(len(text)):
        if text[i].startswith('interface Ethernet') or text[i].startswith('interface GigabitEthernet'):
            if text[i + 1].startswith(' description') == False:
                descriptions.append('!')
            else:
                descriptions.append(text[i + 1].strip()[11:])
    return descriptions

old_conf = open('oldconfig.cfg', 'r', encoding='utf-8')
conf_text = old_conf.readlines()
sys_name = get_sysname(conf_text)
ip = get_ip(conf_text)
gw = get_gw(conf_text)
print(sys_name)
print(ip, gw)
description_list = get_description(conf_text)
vlans_list = get_vlans(conf_text)
management = ''.join([vlans_list[i - 1] for i in range(0, len(vlans_list)) if vlans_list[i] == "management"])
iptv = ''.join([vlans_list[i - 1] for i in range(0, len(vlans_list)) if vlans_list[i] == "IPTV"])
vlans_names = ""

all_vlans = " ".join(vlans_list[0::2])
all_vlans = all_vlans.split()
print(all_vlans)
for el in range(0, len(vlans_list)):
    if vlans_list[el] != "management" and vlans_list[el] != 'IPTV' and vlans_list[el].isdigit() == False:
        vlans_names += f'vlan {vlans_list[el-1]}\n  name "{vlans_list[el]}"\n!\n'


print(vlans_list)
print(description_list)

empty_config = open('MES2424.txt', 'r', encoding='utf-8')
conf_text = empty_config.read()
new_text = conf_text.replace('<hostname>', sys_name)
new_text = new_text.replace('<ip>', ip)
new_text = new_text.replace('<gw>', gw)
new_text = new_text.replace('<management>', management)
new_text = new_text.replace('<iptv>', iptv)
new_text = new_text.replace('<vlans_names>', vlans_names.strip())
#new_text = new_text.replace('<all_vlans>', all2_vlans)
for el in range(0,len(description_list)):
        new_text = new_text.replace('<desc>', f'"{description_list[el]}"', 1)
filename = sys_name + '.conf'
output = open(filename, 'w', encoding='utf-8')
print(new_text, file=output)
empty_config.close()
output.close()

