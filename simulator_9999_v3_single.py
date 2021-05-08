#! python3

# coding:utf-8
#v3: add tas function
import socket
import re
from multiprocessing import Process
import time



def genresp(req):
    with open ("searchresp.xml","r") as f:
        disresp=f.readlines()
        #print (resp)
    with open ("modifyresp.xml","r") as f:
        modifyresp=f.readlines()
    with open ("autoprovresp.xml","r") as f:
        autoprovresp=f.readlines()
    if re.search('searchRequest',req.decode()):
        return disresp
    elif re.search('modifyRequest',req.decode()):
        return modifyresp
    elif re.search('addRequest',req.decode()):
        return modifyresp
    elif re.search('deleteRequest',req.decode()):
        return modifyresp
    elif re.search('ProvisionType',req.decode()):
        global i
        i=i+1
        print("##################"+str(i%3))
        if i%3 != 0:
            time.sleep(1)
            #pass
        return autoprovresp
    else:
        return "invalid request"
		
def genresp_tas(req):
    with open ("rtrv-ngfs.xml","r") as f:
        disresp=f.readlines()
        #print (resp)
    with open ("ed-ngfs.xml","r") as f:
        modifyresp=f.readlines()
    with open ("ent-ngfs.xml","r") as f:
        addresp=f.readlines()
    with open ("dlt-ngfs.xml","r") as f:
        delresp=f.readlines()
    if re.search('rtrv-ngfs',req.decode()):
        return disresp
    elif re.search('ed-ngfs',req.decode()):
        return modifyresp
    elif re.search('ent-ngfs',req.decode()):
        return addresp
    elif re.search('dlt-ngfs',req.decode()):
        return delresp
    else:
        return "invalid request"

def handle_client(client_socket,t):
    print ("handle client message...")
    request_data = client_socket.recv(15000)
    print("request data:", request_data)
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Accept-Encoding: gzip,deflate\r\nContent-Type: text/xml;charset=UTF-8\r\nSOAPAction: ""\r\n"
    if t=='tas':
        response_data= genresp_tas(request_data)
    else:
        response_data= genresp(request_data)
    response = response_start_line + response_headers + "\r\n" + "".join(response_data)
    client_socket.send(bytes(response, "utf-8"))
    client_socket.close()


if __name__ == "__main__":
    type='hss'
    t = input ("please enter the saam type hss or tas: ")
    if t.lower() =='tas':
        type='tas'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("10.16.9.110", 9999))
    server_socket.listen(10)
    i=0
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket,type)
        client_socket.close()
'''
    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]user connected" % client_address)
        print (client_socket)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()
'''
