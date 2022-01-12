""" Tests """

import script
import log_parser


client=script.ssh_conn()
logTotal,logTotal_response=log_parser.recup_log(client)

def test_get_log():
    """ test for get log """
    test=script.get_log(client)
    assert isinstance(test,list),"Test failed"

def test_get_processor_used():
    """ test for getting processor used """
    test=script.get_processor_used(client)
    assert  isinstance(test,float),"Test failed"

def test_get_ps():
    """ test for getting process """
    test=script.get_ps(client)
    assert test>0,"Test failed"

def test_get_ip_config_data():
    """ test for getting ip config data """
    test=script.get_ip_config_data(client)
    assert isinstance(test,dict),"Test failed"

def test_get_process_running():
    """ test for getting process running """
    test=script.get_process_running(client)
    assert isinstance(test,dict),"Test failed"

def test_get_memory_total():
    """ test for getting memory total """
    test=script.get_memory_total(client)
    assert test>0,"Test failed"

def test_get_memory_used():
    """ test for geting memroy used """
    test=script.get_memory_used(client)
    assert test>=0,"Test failed"

def test_get_memory_free():
    """ test for getting memory free """
    test=script.get_memory_free(client)
    assert isinstance(test,int),"Test failed"

def test_get_memory_shared():
    """ test for getting memory shared """
    test=script.get_memory_shared(client)
    assert isinstance(test,int),"Test failed"

def test_get_memory_buff_cache():
    """ test for getting memory buffer cachce """
    test=script.get_memory_buff_cache(client)
    assert isinstance(test,int),"Test failed"

def test_get_memory_available():
    """ stest for getting memory available """
    test=script.get_memory_available(client)
    assert isinstance(test,int),"Test failed"

def test_get_cpu_model_name():
    """ test for getting cpu model name """
    test=script.get_cpu_model_name(client)
    assert isinstance(test,str),"Test failed"

def test_get_cache_size():
    """ test for getting cache size """
    test=script.get_cache_size(client)
    assert isinstance(test,int),"Test failed"

def test_get_cpu_frequency():
    """ test for getting cpu frequency """
    test=script.get_cpu_frequency(client)
    assert isinstance(test,float),"Test failed"

def test_get_number_of_cores():
    """ test for getting number of cores """
    test=script.get_number_of_cores(client)
    assert  test>0, "Test failed"

def test_number_of_diff_ip():
    """ test for getting number of differents ip addresses """
    test=log_parser.number_of_diff_ip(logTotal)
    assert  test>(0,[]), "Test failed"

def test_nb_of_errors():
    """ test for getting number of errors """
    test=log_parser.nb_of_errors(logTotal)
    assert  isinstance(test,int), "Test failed"

def test_ip_per_page():
    """ test for getting the number of ip addresses per page """
    test=log_parser.ip_per_page('http://monitorme2.ddns.net/page2.html',logTotal)
    assert  isinstance(test,int), "Test failed"

def test_what_page_visited():
    """ test for getting page visited """
    test=log_parser.what_page_visited("92.137.14.250",logTotal)
    assert  isinstance(test,list), "Test failed"

def test_get_average_ping():
    """ test for getting the average ping """
    test=log_parser.get_average_ping(logTotal_response)
    assert  isinstance(test,float), "Test failed"

def test_get_average_ping_by_page():
    """ test for getting the average ping by page """
    test=log_parser.get_average_ping_by_page('/index.html',logTotal_response)
    assert  isinstance(test,float), "Test failed"
