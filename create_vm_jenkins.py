#!/usr/bin/env python

import natsort
import time

from lndynamic import LNDynamic


# find lunanode credentials
with open(r"/home/hme/.lunanode/commands.txt") as hpass:
      lines = hpass.readlines()
api = LNDynamic(lines[0].rstrip('\n'), lines[1].rstrip('\n'))

# image Ubuntu-remote
def create_ubuntu_remote(name):
    api.request("vm", "create",
                {'hostname': name, 'plan_id': 3, 'region': 'roubaix', 'image_id': 148540, 'storage': 70})

# image Centos-remote 6 = 16 mb , 3 = 8 mb
def create_centos_remote(name):
    api.request("vm", "create",
                {'hostname': name, 'plan_id': 5, 'region': 'roubaix', 'image_id': 148508, 'storage': 250})

# image Centos-controller
def create_centos_controller(name):
    api.request("vm", "create",
                #{'hostname': name, 'plan_id': 3, 'region': 'roubaix', 'image_id': 148508, 'storage': 70})
                {'hostname': name, 'plan_id': 90, 'region': 'toronto', 'image_id': 148497, 'storage': 125})
project_name = 'training-'
user_number = input("Numero de la vm villeurbanne ? ")
user_number= str(user_number)
#create_centos_:controller(project_name + "controller-" +  user_number)
create_centos_controller(project_name + "" +  user_number)
#create_ubuntu_remote(project_name + "remote-ubuntu-" +  user_number)
time.sleep(240)
results = api.request('vm', 'list')
f = open(r"/home/hme/inventory_jenkins_villeurbanne_" + user_number, "w+")
hfile = open(r"/home/hme/user_jenkins_villeurbanne_" + user_number, "w+")
val= results.get('vms')
all_key= ['vm_id','name','primaryip']
#print(val)
user='centos'
user_dic={}
for z in range(0,len(val)):
    if "jenkins-pic" in val[z].get(all_key[1]):
        #print(val[z].get(all_key[0]))
        name=val[z].get(all_key[1])
        ip= val[z].get(all_key[2])
        results = api.request('vm', 'info', {'vm_id': val[z].get(all_key[0])})
        #print(results)
        thepass=results.get('info')
        part=thepass.get('login_details').split(':')
        password=part[2]
        line = "{}  ansible_ssh_user={}  ansible_ssh_pass={} ansible_ssh_extra_args='-o StrictHostKeyChecking=no'\n".format(ip, user , password.strip() )
        f.write(line)

# print (user_dic)
#list_user = user_dic.keys();
#natural = natsort.natsorted(list_user)
# print natural
#for vts in range(0, len(natural)):
#    myip = user_dic[natural[vts]]
#    user_line = "{} \t {} \t centos \n".format(natural[vts], myip)
#    hfile.write(user_line)
#hfile.close()
