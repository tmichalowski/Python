#!/usr/bin/python
import threading, time, paramiko, socket, getpass
from Queue import Queue
locke1 = threading.Lock()
q = Queue()

#Check the login
def check_hostname(host_name):
    with locke1:
        print ("Checking hostname :"+str(host_name)+" with " + threading.current_thread().name)
        file_output = open('output_file','a')
        file_success = open('success_file','a')
        file_failed = open('failed_file','a')
        file_error = open('error_file','a')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
          ssh.connect(host_name, username='username',  timeout=5)
          #print ("Success")
          file_success.write(str(host_name+"\n"))
          file_success.close()
          file_output.write("succes "+str(host_name+"\n"))
          file_output.close()

          # printing output if required from remote machine
          #stdin,stdout,stderr = ssh.exec_command("hostname&&uptime")
          #for line in stdout.readlines():
           # print (line.strip())

        except paramiko.SSHException:
                # print ("error")
                file_failed.write(str(host_name+"\n"))
                file_failed.close()
                file_output.write("failed "+str(host_name+"\n"))
                file_output.close()
                #quit()
        except paramiko.ssh_exception.NoValidConnectionsError:
                #print ("might be windows------------")
                file_output.write("failed "+str(host_name + "\n"))
                file_output.close()
                file_failed.write(str(host_name+"\n"))
                file_failed.close()
                #quit()
        except socket.gaierror:
          #print ("wrong hostname/dns************")
          file_output.write("error "+str(host_name+"\n"))
          file_output.close()
          file_error.write(str(host_name + "\n"))
          file_error.close()

        except socket.timeout:
           #print ("No Ping %%%%%%%%%%%%")
           file_output.write("error "+str(host_name+"\n"))
           file_output.close()
           file_error.write(str(host_name + "\n"))
           file_error.close()

        ssh.close()


def performer1():
    while True:
        hostname_value = q.get()
        check_hostname(hostname_value)
        q.task_done()

if __name__ == '__main__':

    print ("This script checks all the hostnames in the input_file with your ssh key and write the outputs in below files: \n1.file_output\n2.file_success \n3.file_failed \n4.file_error \n")

    f = open('output_file', 'w')
    f.write("-------Output of all hosts-------\n")
    f.close()
    f = open('success_file', 'w')
    f.write("-------Success hosts-------\n")
    f.close()
    f = open('failed_file', 'w')
    f.write("-------Failed hosts-------\n")
    f.close()
    f = open('error_file', 'w')
    f.write("-------Hosts with error-------\n")
    f.close()

    with open("input_file") as f:
        hostname1 = f.read().splitlines()

#Read the standard password from the user
    start_time1 = time.time()

    for i in hostname1:
        q.put(i)
    #print ("all the hostname : "+str(list(q.queue)))
    for no_of_threads in range(10):
        t = threading.Thread(target=performer1)
        t.daemon=True
        t.start()

    q.join()
    print ("Check output files for results")
    print ("completed task in" + str(time.time()-start_time1) + "seconds")
