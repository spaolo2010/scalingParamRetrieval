# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from device_config_discovery import device_connection as dev
import threading
import re
class controller:
    def __init__ (self):
        self.output = {}
        self.ipaddress =""
        all_nodes_connfig = []
    def retrieveDataFromNode(self):
        threaded_nodes = []
        # {'username'  :'admin','password' :'Cisco@123','IP' : '10.104.153.243'}
        # ['term length 0\n', 'show runn | i hostname\n', 'show runn\n', 'show vrf all\n', 'exit\n']
        #credentials = [{'username': 'svsbpanso', 'password': 'Pldt@321', 'IP': '10.104.153.23'}]
        credentials=[]
        self.populateCredentials(credentials)

        # {'username'  :'admin','password' :'Cisco@123','IP' : '10.104.153.243'}]
        for credential in credentials:
            device = dev(credential['username'], credential['password'], credential['IP'],
                         ['term len 0\n', 'show  arp  location  all   | utility  egrep \"(0/[0-9]| ARPA)\"\n',
                          'exit\n'],self)
            # ['show runn | i hostname\n', 'show ver\n', 'show vrf all\n', 'exit\n'])
            device.start()
            threaded_nodes.append(device)
    def getOutput(self):
        if (self.output == {}):

            return None
        return self.output , self.ipaddress
    def setOutput(self,output,ipaddress):
        self.ipaddress=ipaddress
        self.output = output

    def populateCredentials(self, credentials):
        with open('devices_list') as f:
            entry = {}
            lines = f.readlines()
            #print (lines)
            parts = lines[0].split(' ')
            entry ['IP'] = parts[0]
            entry['username'] = parts[1]
            entry ['password'] = parts[2]
            credentials.append(entry)



def main():

    contr = controller()
    contr.retrieveDataFromNode()
    while (contr.getOutput() == None):
        pass
    commands,ipaddress=contr.getOutput()
    global location
    location= None
    count =0
    arps_count = []
    for ele in commands['show  arp  location  all   | utility  egrep "(0/[0-9]| ARPA)"']:

        if (re.match ("0/[0-9]+.*",ele)):
            #print (ele)
            if count != 0:
                pass
                arp_count = {}
                arp_count['location'] = location[:-2]
                arp_count['count'] = count
                arps_count.append(arp_count)
                #print (location[:-2] , count)
            location = ele
            #print (location)
            count = 0
        elif (re.match (".*ARPA.*",ele)):
            count+=1

    arp_count = {}
    arp_count['location'] = location[:-2]
    arp_count['count'] = count
    arps_count.append(arp_count)
    #print (location[:-2], count)
    max =0
    #print (arps_count)
    location=None
    for ele in arps_count:
        #print (ele)
        if (ele['count'] > max):
            max = ele['count']
            location = ele['location']
    print (ipaddress + " "+location +": "+ str(max))
# Press the green button in the gutter to run the script.



if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
