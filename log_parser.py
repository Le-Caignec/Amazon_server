""" LogParser """
import apache_log_parser
import script

FILTRE="%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""
line_parser = apache_log_parser.make_parser(FILTRE)
line_parser_response = apache_log_parser.make_parser('%V %m "%U" "%q" %{Content-Type}o %s %B %O %D')


def recup_log(client):
    """ get the logs from the apache server """
    log_total = script.get_log(client)
    log_resp_time = script.get_response_time_log(client)
    log_total_response=[]
    for line in log_resp_time:
        log_total_response.append(line[22:])
    return log_total,log_total_response

#-------------log serveur--------------------

def number_of_diff_ip(log_total):
    """ return the number of differents ip address & the ip addresses """
    host_array = []
    for line in log_total:
        log_line_data = line_parser(line)
        #print(log_line_data.get('remote_host'))
        if host_array.__contains__(log_line_data.get('remote_host')) is False:
            host_array.append(log_line_data.get('remote_host'))
    return len(host_array), host_array

def nb_of_errors(log_total):
    """ return the number of errors on the server """
    nombre=0
    for line in log_total:
        log_line_data = line_parser(line)
        if log_line_data.get('status')=='404':
            nombre+=1
    return nombre

def ip_per_page(page,log_total):
    """ return the number of ip address per page """
    host_array = []
    for line in log_total:
        log_line_data = line_parser(line)
        if log_line_data.get('request_header_referer')==page and host_array.__contains__(log_line_data.get('remote_host')) is False:
            host_array.append(log_line_data.get('remote_host'))
    return len(host_array)

def what_page_visited(ip_address,log_total):
    """ return the different pages visited by an ip address """
    page_array = []
    for line in log_total:
        log_line_data = line_parser(line)
        if log_line_data.get('remote_host')==ip_address and page_array.__contains__(log_line_data.get('request_header_referer')) is False:
            page_array.append(log_line_data.get('request_header_referer'))
    return page_array

def get_average_ping(log_total_response):
    """ get the average ping """
    ping_total = 0
    nb_of_items = 0
    for line in log_total_response:
        log_line_data = line_parser_response(line)
        ping_total += int(log_line_data.get('time_us'))
        nb_of_items +=1
    ping_total = ping_total/nb_of_items
    return ping_total/10

def get_average_ping_by_page(page,log_total_response):
    """ get the average ping by page """
    ping_total = 0
    nb_of_items = 0
    for line in log_total_response:
        log_line_data = line_parser_response(line)
        if log_line_data.get('url_path')==page:
            ping_total += int(log_line_data.get('time_us'))
            nb_of_items +=1
    ping_total = ping_total/nb_of_items
    return ping_total/10
