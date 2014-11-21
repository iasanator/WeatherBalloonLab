# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 09:48:10 2014

@author: nick
"""

import re
import thread
import socket
import unicodedata
import time
import platform
import sys
print('Running in Python ' + platform.python_version())

DEBUG = True

TCP_IP = 'localhost'
TCP_PORT = 23457
BUFFER_SIZE = 1024

isServerRunning = False

def main():
    global isServerRunning

    thread.start_new_thread(server, ())
    
    while(True):
        time.sleep(1)
        if isServerRunning == False:
            thread.start_new_thread(server, ())

def server():
    global isServerRunning
    
    isServerRunning = True
    
    try:
        #Start the Server
        print("Starting Server")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, TCP_PORT)
        s.bind(('localhost', TCP_PORT))
        s.listen(1)
        
        #Pause and Wait for Connection
        print("Waiting for Connection...")
        conn, addr = s.accept()
        print 'Connected with:', addr
        
        #Recieve and Send Data 
        while (True):
            print("Waiting For Data...")
            data = conn.recv(BUFFER_SIZE)
            
            if not data:
                isServerRunning = False
                break
            
            print('Received Data: ' + data)
    
            command = unicodedata.normalize("NFD", unicode(re.sub(r'[^a-zA-Z0-9]',"", unicode(data))))
    
            if command != "":
                
                #Make Response
                print("Command: " + command)
                response = ""
                
                if command == "hi":
                    response = "wassup dawg"
                elif command == "shutdown":
                    if DEBUG:
                        shutdown()
                        response = "AS YOU WISH MY BELEVOLENT DICTATOR"
                    else:
                        response = "NO"
                else:
                    response = "INVALID"
                    
                #Format Response    
                response = (response + "\n").encode('utf-8')
                
                #Respond
                print('Sending: ' + response)
                conn.send(response)
                
        print("Connection Closed")
    except:
        isServerRunning = False
        print sys.exc_info()[0]
        
def debugPrint(line):
    if DEBUG == True:
        print(line)

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

main()
