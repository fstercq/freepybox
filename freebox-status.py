#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Displays a summary of status information
Created by pagecp (github) based on example-wan.py
'''
from freepybox import Freepybox
import time
import locale

locale.setlocale(locale.LC_ALL, str('fr_FR.UTF-8'))
    
# Instantiate Freepybox class using default application descriptor 
# and default token_file location
fbx = Freepybox()

# Connect to the freebox with default http protocol
# and default port 80
# Be ready to authorize the application on the Freebox if you use this
# example for the first time
fbx.open('mafreebox.freebox.fr', 443)

print('______________________________________________________________________');
print('');
print('                      Etat de la Freebox');
print('______________________________________________________________________');
print('');

print('');
print('Informations générales :');
print('========================');
print('');

fbx_config = fbx.system.get_config()
fbx_connection_status_details = fbx.connection.get_status_details()
fbx_connection_logs = fbx.connection.get_logs()
fbx_connection_config = fbx.connection.get_config()
fbx_ipv6 = fbx.connection.get_ipv6_config()
fbx_dhcp_config = fbx.dhcp.get_config()
fbx_phone = fbx.phone.get_config();
fbx_wifi = fbx.wifi.get_global_config();
fbx_wifi_ap = fbx.wifi.get_ap(0);
fbx_bss = fbx.wifi.get_bss();
lan_config = fbx.lan.get_config();
dmz_config = fbx.fw.get_dmz();
fbx_static_dhcp = fbx.dhcp.get_static_dhcp_lease();
fbx_ports = fbx.fw.get_forward()
fbx_switch_status = fbx.switch.get_status()

print('  Modèle                         {0}'.format(fbx_config['board_name']));
print('  Version du firmware            {0}'.format(fbx_config['firmware_version']));
print('  Mode de connection             {0}'.format(fbx_connection_status_details['media']));
print('  Temps depuis la mise en route  {0}'.format(fbx_config['uptime']));
print('');

print('');
print('Téléphone :');
print('===========');
print('');
#print('  Etat                           ');
if fbx_phone[0]['on_hook'] == True:
    phone_status = 'Raccroché';
else:
    phone_status = 'Décroché';
print('  Etat du combiné                {0}'.format(phone_status));
if fbx_phone[0]['is_ringing'] == True:
    ring_status = 'Active';
else:
    ring_status = 'Inactive';
print('  Sonnerie                       {0}'.format(ring_status));
print('');

print('');
print('Ftth :');
print('======');
print('');

print('                         Descendant         Montant');
print('                         --                 --');
print('  Débit ATM              {0:6.1f} Mb/s       {1:6.1f} Mb/s'.format(fbx_connection_status_details['bandwidth_down']/1000000,fbx_connection_status_details['bandwidth_up']/1000000));
print('');

print(' Journal de connexion ftth');
print(' ---------------------------');
print('');

print('  Date                      Type      Nom       Etat        Débit (Mb/s)');
print('  --                        --        --        --          --');
index = 0
while index < len(fbx_connection_logs):
    dat = time.strftime("%c", time.localtime(fbx_connection_logs[index]['date']));
    typ = fbx_connection_logs[index]['type'];
    if typ == 'link':
        typ_str = 'Lien';
    elif typ == 'conn':
        typ_str = 'Connexion';
    else :
        typ_str = typ;
    name = fbx_connection_logs[index][typ];
    state = fbx_connection_logs[index]['state'];
    if state == 'up':
        status = 'Connexion';
    else :
        status = 'Deconnexion';
    if typ == 'link':
        down = fbx_connection_logs[index]['bw_down']/1000000;
        up = fbx_connection_logs[index]['bw_up']/1000000
        print('  {0}  {1:10.10s}{2:10.10s}{3:11.11s} {4:.0f}/{5:.0f}'.format(dat,typ_str,name,status,down,up));
    else :
        print('  {0}  {1:10.10s}{2:10.10s}{3:11.11s}'.format(dat,typ_str,name,status));
    index+=1
print('');

print('');
print('Wifi :');
print('======');

print('');
if fbx_wifi['enabled'] == True :
  status = 'Ok';
else :
  status = 'Off';
wifi_state = fbx_wifi_ap['status']['state'];
if wifi_state == 'active':
    wifi_active = 'Activé';
else :
    wifi_active = 'Désactivé';
print('  Etat                           {0}'.format(status));
print('  Ssid                           {0}'.format(fbx_bss[0]['config']['ssid']));
key = fbx_bss[0]['config']['encryption'].upper();
key = key.replace('_',' [',1);
key = key.replace('_','-');
key += ']';
print('  Type de clé                    {0}'.format(key));
print('  Canal primaire                 {0}'.format(fbx_wifi_ap['status']['primary_channel']));
secondary_channel = fbx_wifi_ap['status']['secondary_channel'];
if secondary_channel == 0:
    secondary_channel = 'Désactivé'
print('  Canal secondaire               {0}'.format(secondary_channel));
print('  Largeur de bande               {0} MHz'.format(fbx_wifi_ap['status']['channel_width']));
print('  Etat du réseau                 {0}'.format(wifi_active));
#print('  FreeWifi                       Actif');
#print('  FreeWifi Secure                Actif');
print('');

print('');
print('Réseau :');
print('========');

print('');
print('  Adresse MAC Freebox            {0}'.format(fbx_config['mac']));
print('  Adresse IP                     {0}'.format(fbx_connection_status_details['ipv4']));
print('  Adresse IPV6                   {0}'.format(fbx_connection_status_details['ipv6']));
ipv6_status = fbx_ipv6['ipv6_enabled'];
if ipv6_status == True:
    status = 'Activé';
else :
    status = 'Désactivé';
print('  IPv6                           {0}'.format(status));
if lan_config['mode'] == 'router':
    status = 'Activé';
else :
    status = 'Désactivé';
print('  Mode routeur                   {0}'.format(status));
print('  Adresse IP privée              {0}'.format(lan_config['ip']));
ip_dmz = dmz_config['ip'];
if ip_dmz == '':
  ip_dmz = 'Désactivé'    
print('  Adresse IP DMZ                 {0}'.format(ip_dmz));
if fbx_connection_config['ping'] == True:
  status = 'Activé';
else :
  status = 'Désactivé';
print('  Réponse au ping                {0}'.format(status));
if fbx_connection_config['wol'] == True:
  status = 'Activé';
else :
  status = 'Désactivé';
print('  Proxy Wake On Lan              {0}'.format(status));
if fbx_dhcp_config['enabled'] == True:
  status = 'Activé';
else :
  status = 'Désactivé';
print('  Serveur DHCP                   {0}'.format(status));
print('  Plage d\'adresses dynamique     {0} - {1}'.format(fbx_dhcp_config['ip_range_start'],fbx_dhcp_config['ip_range_end']));

print('');
print(' Attributions dhcp :');
print(' -------------------');

print(''); 
print('  Hostname               Adresse MAC            Adresse IP');
print('  --                     --                     --');
index = 0
while index < len(fbx_static_dhcp):
    mac = fbx_static_dhcp[index]['mac'];
    hostname = fbx_static_dhcp[index]['hostname'];
    ip = fbx_static_dhcp[index]['ip'];
    print('  {0:21.21s}  {1:21.21s}  {2:21.21s}'.format(hostname,mac,ip));
    index += 1;

print('');
print(' Redirections de ports :');
print(' -----------------------');

print('');
print('  Protocole  IP source         Port source  Destination       Nom               Port destination');
print('  --         --                --           --                --                --');
index = 0
while index < len(fbx_ports):
    if fbx_ports[index]['enabled'] == True:
        ip_proto = fbx_ports[index]['ip_proto'];
        wan_port_start = fbx_ports[index]['wan_port_start'];
        wan_port_end = fbx_ports[index]['wan_port_end'];
        lan_ip = fbx_ports[index]['lan_ip'];
        src_ip = fbx_ports[index]['src_ip'];
        if src_ip == '0.0.0.0':
            src_ip = 'Tout';
        lan_port = fbx_ports[index]['lan_port'];
        hostname = fbx_ports[index]['hostname'];
        print('  {0:9.9s}  {1:16.16s}  {2:<5d} {3:<5d}  {4:16.16s}  {5:16.16s}  {6}'.format(ip_proto.upper(),src_ip,wan_port_start,wan_port_end,lan_ip,hostname,lan_port));
    index += 1;

print('');
print(' Interfaces réseau :');
print(' -------------------');

print('');
print('                         Lien           Débit entrant  Débit sortant');
print('                         --             --             --');

# Mise a jour des debits tous en meme temps pour qu ils correspondent... mais ca ne fonctionne pas..!
stats = [None] * len(fbx_switch_status);
index = 0
while index < len(fbx_switch_status):
    stats[index] = fbx.switch.get_port_stats(fbx_switch_status[index]['id'])
    index += 1;
fbx_connection_status_details = fbx.connection.get_status_details()

rx = fbx_connection_status_details['rate_down']/1024
tx = fbx_connection_status_details['rate_up']/1024
rx_str = '{0:.0f} ko/s'.format(rx)
tx_str = '{0:.0f} ko/s'.format(tx)
print('  {0:21.21s}  {1:13.13s}  {2}  {3}'.format('WAN', '', rx_str.ljust(13," "), tx_str.ljust(13," ")));
index = 0
while index < len(fbx_switch_status):
    name = fbx_switch_status[index]['name'];
    link = fbx_switch_status[index]['mode'];
    if fbx_switch_status[index]['link'] == 'up':
        rx = stats[index]['rx_bytes_rate']/1024
        tx = stats[index]['tx_bytes_rate']/1024
        rx_str = '{0:.0f} ko/s'.format(rx)
        tx_str = '{0:.0f} ko/s'.format(tx)
        print('  {0:21.21s}  {1:13.13s}  {2}  {3}'.format(name, link, rx_str.ljust(13," "), tx_str.ljust(13," ")));
    else :
        print('  {0:21.21s}  Non connecté'.format(name));
    index += 1;

print('');

# Close the freebox session
fbx.close()

