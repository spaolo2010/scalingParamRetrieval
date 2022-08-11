from socket import socket

import paramiko
import threading
import re
from threading import Lock
import traceback as tb

#from series_of_commands import command_processing


class device_connection(threading.Thread):

    def __init__(self, username, password, ipaddress, commands,controller):
        self.mutex = Lock()
        self.username = username
        self.password = password
        self.ipaddress = ipaddress
        self.commands = commands
        threading.Thread.__init__(self)
        self.commands_output = {}
        self.commands_threads = []
        self.controller = controller

    def run(self):
        try:

            client = paramiko.SSHClient()

            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.ipaddress, port=22, username=self.username, password=self.password)

            # transport = paramiko.Transport((self.ipaddress, port))
            # transport.connect(None, self.username, self.password)
            # sftp = paramiko.SFTPClient.from_transport(transport)
            channel = client.invoke_shell()
            # for command in self.commands:
            # stdin, stdout, stderr = client.exec_command(command)
            # print (stdout.readlines())
            # print(stderr)

            # stdout = stdout.readlines()
            stdin = channel.makefile('wb')
            stdout = channel.makefile('r')
            for command in self.commands:
                stdin.write(command)

            finalstring = ""
            global c
            c = 0
            output = []
            test = True
            # self.mutex.acquire()
            for line in stdout:
                # print (line,end='.')
                # print(line,end=".")
                # finalstring+=line
                # print(line)
                # print (line)
                output.append(line)
            # print (output)
            c = 0
            start = False
            finaloutput = []

            for ele in output:
                if (start == False):

                    command = self.commands[c][:-1]
                    a = f".*[a-zA-Z0-9].*{command}.*"
                    if re.match(a, ele):
                        start = True
                        finaloutput.append(ele)
                        # print (finaloutput)

                elif (start == True and c < len(self.commands) - 1):
                    startcommand = self.commands[c][:-1]
                    endcommand = self.commands[c + 1][:-1]
                    a = f".*[a-zA-Z0-9].*{endcommand}.*"
                    if (not re.match(a, ele)):
                        finaloutput.append(ele)
                    else:
                        # print(finaloutput)
                        self.commands_output[startcommand] = finaloutput

                        finaloutput = []
                        c += 1
            #print(self.commands_output)

            self.controller.setOutput(self.commands_output)
        except paramiko.AuthenticationException as ex:
            ex.with_traceback(tb)
            client.close()
        except paramiko.SSHException as sshe:
            sshe.with_traceback(tb)
            client.close()

    def fill_list_of_outputs(self, result):
        # print ("AAAAAAAAA")
        # self.mutex.acquire()
        self.commands_output.append(result)
        # self.mutex.release()


