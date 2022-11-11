import os
import socket
from contextlib import closing
import subprocess
import mysql.connector
def database_insert(usr,port):
    mydb = mysql.connector.connect(host="localhost",port=9090,user="root",password="sriganesan",database='vcl')
    cursor=mydb.cursor()
    query="insert into instances values('"+usr+"',"+str(port)+")"
    cursor.execute(query)
    cursor.close()
    mydb.commit()
    mydb.close()
def database_record(usr):
    mydb = mysql.connector.connect(host="localhost",port=9090,user="root",password="sriganesan",database='vcl')
    cursor=mydb.cursor()
    query="select * from instances where name='"+usr+"'"
    cursor.execute(query)
    result=cursor.fetchall()
    cursor.close()
    mydb.commit()
    mydb.close()
    if(result==[]):
        return True
    else:
        return False
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def instance_creation(usr_name):
    port=find_free_port()
    if(database_record(usr_name)):
        os.system('docker run --privileged --name '+usr_name+'_server -p '+str(port)+':'+'3000 -d linuxserver/webtop:ubuntu-kde-version-bb816450')
        database_insert(usr_name,port)
        return port
        
    else:
        mydb = mysql.connector.connect(host="localhost",port=9090,user="root",password="sriganesan",database='vcl')
        cursor=mydb.cursor()
        query="select * from instances where name='"+usr_name+"'"
        cursor.execute(query)
        result=cursor.fetchall()
        cursor.close()
        mydb.commit()
        mydb.close()
        return result[0][1]

