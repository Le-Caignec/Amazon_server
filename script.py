""" script """
from configparser import ConfigParser
import paramiko

results = []
parser = ConfigParser()
parser.read('configuration.ini')
WHICH_MACHINE="machine1"

def ChangeMachine(value):
    """ swith between different servers """
    global WHICH_MACHINE
    if(value == "monitorme1.ddns.net"):
        WHICH_MACHINE="machine1"
    if(value == "monitorme2.ddns.net"):
        WHICH_MACHINE="machine2"
    if(value == "monitorme3.ddns.net"):
        WHICH_MACHINE="machine3"
    if(value == "defense1.hopto.org"):
        WHICH_MACHINE="machine4"

# pour recupérer les info du config.ini
address=parser[WHICH_MACHINE]['ADDRESS_IP']
PORT = parser[WHICH_MACHINE]['PORT']
user=parser[WHICH_MACHINE]['USERNAME']
PASSWORD=parser[WHICH_MACHINE]['PASSWORD']
COMMAND=parser[WHICH_MACHINE]['COMMAND']


def ssh_conn():
    """ ssh conn """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(address, port=PORT, username=user, password=PASSWORD)
    #print("la connexion est faite")
    return client

#-------------log------------
def get_log(client): #graph
    """ Renvoie le fichier log """
    _, stdout_test, _ =client.exec_command('cat /var/log/apache2/access.log')
    line_mem_total = stdout_test.readlines()
    return line_mem_total

#-------------log_resptime------------
def get_response_time_log(client):#graph
    """ log  """
    _, stdout_test, _ =client.exec_command('cat /var/log/apache2/responsetime.log')
    line_mem_total = stdout_test.readlines()
    return line_mem_total

#-----------------------------------
def get_processor_used(client):#graph
    """ processor used """
    _, stdout_top, _ = client.exec_command(
        "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")
    return float(top)

#-----------------------------------
def get_ps(client):#graph
    """ Return data from ps command """
    _, stdout_number_process, _ = client.exec_command('ps | wc -l')
    line_number_process = stdout_number_process.readlines()
    number_process = int(''.join(line_number_process)) - 1
    return number_process

#-----------------------------------
def get_ip_config_data(client):#static
    """ Return data about ifconfig command """
    if_config = {}
    _, stdout_if_config_tx, _ = client.exec_command(
        "ifconfig | grep TX | grep bytes ")
    _, stdout_if_config_rx, _ = client.exec_command(
        "ifconfig | grep RX | grep bytes ")
    line_stdout_if_config_tx = stdout_if_config_tx.readlines()
    line_stdout_if_config_rx = stdout_if_config_rx.readlines()

    if_config_rx_packet = int(''.join(line_stdout_if_config_rx).split(" ")[10])
    if_config_rx_bytes = int(''.join(line_stdout_if_config_rx).split(" ")[13])

    if_config_tx_packet = int(''.join(line_stdout_if_config_tx).split(" ")[10])
    if_config_tx_bytes = int(''.join(line_stdout_if_config_tx).split(" ")[13])

    if_config[address] = {
        "tx_packet": if_config_tx_packet,
        "rx_packet": if_config_rx_packet,
        "rx_bytes": if_config_rx_bytes,
        "tx_bytes": if_config_tx_bytes
    }

    print(_, _)

    return if_config

#-----------------------------------

def get_process_running(client):#static
    """ Return a map of all process running with their processor consumption and name """
    _, stdout_top, _ = client.exec_command(
        "top -n1 -b | awk "+"'"+"BEGIN {line=0;}{line++;if(line>7){print $1,$9,$12}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", " ")
    top = top.split(" ")
    process = {}
    for i in range(0, len(top)-2):
        if i % 3 == 0:
            process[top[i]] = [top[i+1], top[i+2]]

    return process
#-----------------------------------

def get_memory_total(client):#static
    """ Return a the total memory in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $2}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_memory_used(client):#graph
    """ Return a the memory used in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $3}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_memory_free(client):#graph
    """ Return a the memory free in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $4}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_memory_shared(client):#graph
    """ Return a the memory shared in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $5}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_memory_buff_cache(client):#graph
    """ Return a the memory buff/cache in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $6}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_memory_available(client):#graph
    """ Return a the memory available in Kb """
    _, stdout_top, _ = client.exec_command(
        "free | awk "+"'"+"BEGIN {line=0;}{line++;if(line==2){print $7}}"+"'")
    line_top = stdout_top.readlines()
    top = ''.join(line_top)
    top = top.replace("\\n", "")

    return int(top)

#-----------------------------------
def get_cpu_model_name(client):#static
    """ Return a the name of the processor """
    _, stdout_cpu, _ = client.exec_command(
        "cat /proc/cpuinfo | grep model\\ name | awk "+"'"+"{$1=$2=$3="+'""'+";print $0}"+"'")
    line_cpu = stdout_cpu.readlines()
    cpu = ''.join(line_cpu)
    cpu = cpu.replace("   ", "")

    return cpu

#-----------------------------------
def get_cache_size(client):#static
    """ Return a the cache size of the processor """
    _, stdout_cpu, _ = client.exec_command(
        "cat /proc/cpuinfo | grep cache\\ size | awk "+"'"+"{$1=$2=$3=$5="+'""'+";print $0}"+"'")
    line_cpu = stdout_cpu.readlines()
    cpu = ''.join(line_cpu)
    cpu = cpu.replace("   ", "")

    return int(cpu)

#-----------------------------------
def get_cpu_frequency(client):#static
    """ Return a the frequency of the processor """
    _, stdout_cpu, _ = client.exec_command(
        "cat /proc/cpuinfo | grep cpu\\ MHz | awk "+"'"+"{$1=$2=$3="+'""'+";print $0}"+"'")
    line_cpu = stdout_cpu.readlines()
    cpu = ''.join(line_cpu)
    cpu = cpu.replace("   ", "")
    cpu = cpu.replace("\\n", "")

    return float(cpu)

#-----------------------------------
def get_number_of_cores(client):#static
    """ Return a the number of cores of the processor """
    _, stdout_cpu, _ = client.exec_command(
        "cat /proc/cpuinfo | grep cpu\\ cores | awk "+"'"+"{$1=$2=$3="+'""'+";print $0}"+"'")
    line_cpu = stdout_cpu.readlines()
    cpu = ''.join(line_cpu)
    cpu = cpu.replace("   ", "")
    cpu = cpu.replace("\\n", "")

    return int(cpu)

#client=ssh_conn()
#l=get_processor_used(client)
#print(l)
