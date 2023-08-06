import socket
import time
import abc
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import Process
from threading import Thread
from queue import Queue
import os

from confluent_kafka import SerializingProducer, KafkaException

from kp_fraydit import custom_errors
from kp_fraydit.custom_types import check_int, key_exists
from kp_fraydit.metaclasses import SingletonMeta


# END IMPORTS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# HELPER FUNCTIONS //////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def check_host_port(host: str, port: int, tag='', tries=3, sleep_interval=1):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(3)
    location = (host, port)
    actual_tries = 0
    while tries > actual_tries:
        
        try:
            result_of_check = a_socket.connect_ex(location)
            if result_of_check == 0: return True, host, port, tag, time.time()
            actual_tries += 1
            time.sleep(sleep_interval)
        
        except:
            actual_tries += 1
            time.sleep(sleep_interval)
                
    return False, host, port, tag


def get_ip_and_port_from_string(ip_string: str):
    
    stripped_string = ip_string.strip()
    if stripped_string[:7] == 'http://': stripped_string = ip_string[7:]
    if stripped_string[:8] == 'https://': stripped_string = ip_string[8:]
    
    if len(stripped_string.split(':')) > 1: return stripped_string.split(':')[0], stripped_string.split(':')[1]
    else: return stripped_string, ''


def valid_address_format(url):
    stripped_string = url.strip()
    port = stripped_string.split(':')[-1:][0]
    if not check_int(port): return False
    
    if stripped_string[:7] == 'http://' or stripped_string[:8] == 'https://': 
        return True
    
    return False


# END HELPER FUNCTIONS //////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# PRODUCERNATIVE AND HELPER CLASSES /////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


'''
The actual class that is used to do the produccing. It is transactional and is built to ensure an Exact Once Semantics. 
It is used by the KafkaConnection only and in a threaded manner.
'''

class ProducerNative(SerializingProducer):
    def __init__(self, conf_, value_schema_name, key_schema_name, tx_id):
        self.tx_id = tx_id
        conf_['transactional.id'] = tx_id
        self.__conf = conf_
        self.__value_schema_name = value_schema_name
        self.__key_schema_name = key_schema_name
        super().__init__(conf_)
        # self.queue = Queue()    


    def produce(self, topic, values, keys): # Overrides parent
        self.init_transactions()

        '''
        The infinite loop tries a transaction as long as the error is not abortable. If it is abortable, it is then requeued to the connection
        '''
        while True:
            try:
                self.begin_transaction()
                super().produce(topic, keys, values)
                self.commit_transaction()
                self.flush()
                break
            
            except KafkaException as e:
                if e.args[0].retrievable():
                    continue # retry the transaction until an abortable failure happens
                    '''
                    Upon transaction failure or unidentified failure, the transaction is requeued to be processed
                    '''
                elif e.args[0].txn_requires_abort():
                    self.abort_transaction()
                    KafkaConnection.produce_queue.put([topic, self.__value_schema_name, self.__key_schema_name, values, keys, self.__conf])
                else:
                    self.abort_transaction()
                    KafkaConnection.produce_queue.put([self.__topic_name, self.__value_schema_name, self.__key_schema_name, values, keys, self.__conf])

    
# END PRODUCERNATIVE AND HELPER CLASSES /////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# CONNECTION CLASS //////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


'''
The metaclass that makes the Connection to Kafka a Singleton
'''
# class ConnectionMeta(type):
#     def __init__(cls, name, bases, attrs, **kwargs):
#         super().__init__(name, bases, attrs)
#         cls._instance = None
        

#     def __call__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super().__call__(*args, **kwargs)
        
#         return cls._instance


class KafkaConnection(metaclass=SingletonMeta):

    # INITIALIZATION ////////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    def __init__(self, thread_count=250):
        
        self._kafka_broker_listener = os.environ.get('KAFKA_BROKER_LISTENER')
        if self._kafka_broker_listener is None: self._kafka_broker_listener = "10.100.100.1:9092"
        self._kafka_registry_listener = os.environ.get('KAFKA_REGISTRY_LISTENER')
        if self._kafka_registry_listener is None: self._kafka_registry_listener = "http://10.100.100.1:8081"
        self._status = {}
        self._thread_count = thread_count

        self.__observers = set()
        self.__subject_state = {}
        self. __subject_state['broker_online'] = False
        self.__subject_state['registry_online'] = False
    
        self.loop_active = True
        self.__check_connections()
        self.__produce_queue = queue.Queue()
        self.__start_producer_queue()

    # END INITIALIZATION ////////////////////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # KAFKA CONNECTION ATTRIBUTES AND METHODS ///////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    
    @property
    def kafka_broker_listener(self):
        return self._kafka_broker_listener


    @kafka_broker_listener.setter
    def kafka_broker_listener(self, value):
        ip, port = get_ip_and_port_from_string(value)
        formatted_address = f'{ip}:{port}'
        os.environ['KAFKA_BROKER_LISTENER'] = formatted_address
        self._kafka_broker_listener = formatted_address
        
        
    @property
    def kafka_registry_listener(self):
        return self._kafka_registry_listener


    @kafka_registry_listener.setter
    def kafka_registry_listener(self, value):
        if not valid_address_format(value):
            print (f'Address supplied ({value}) for kafka registry listener is not valid. Please format with http or https preceding address and a port number')
            return
        os.environ['KAFKA_REGISTRY_LISTENER'] = value
        self._kafka_registry_listener = value

    @property
    def subject_state(self):
        return self.__subject_state


    @subject_state.setter
    def subject_state(self, value):
        
        if not isinstance(value, dict): 
            print ('The subject state must be a dict: "registry_online": bool, "broker_online": bool')
            return
            if value.get('broker_online') is None or value.get('registry_online') is None:
                print ('The subject state must be a dict: "registry_online": bool, "broker_online": bool')
                return
        
        previous_state = self.__subject_state
        self.__subject_state['broker_online'] = value['broker_online']
        self.__subject_state['registry_online'] = value['registry_online']
        if previous_state != self.__subject_state:
            self.__notify()
        

    @property
    def broker_online(self):
        return self.subject_state['broker_online']


    @broker_online.setter
    def broker_online(self, value):
        if not isinstance(value, bool):
            print ('Broker online must be a boolean')
            return
        self.subject_state = {'broker_online': value, 'registry_online': self.__subject_state['registry_online']}


    @property
    def registry_online(self):
        return self.subject_state['registry_online']


    @registry_online.setter
    def registry_online(self, value):
        if not isinstance(value, bool):
            print ('Registry online must be a boolean')
            return
        self.subject_state = {'registry_online': value, 'broker_online': self.__subject_state['broker_online']}


    def __check_conn_loop(self):
        
        '''
        Checks the status of the connection. This runs only when the connection loop_active is true. 
        It is used in check_connections where it is infinitely looped in a daemon thread.
        '''
        while self.loop_active:
            
            changed = False

            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(10)
            a_socket2.settimeout(10)

            # Kafka broker
            ip, port = get_ip_and_port_from_string(self.kafka_broker_listener)
            location = (str(ip), int(port))
            result_of_check = a_socket.connect_ex(location)
            
            if result_of_check == 0: 
                broker_online = True
            else: 
                broker_online = False
            
            # Kafka registry
            ip2, port2 = get_ip_and_port_from_string(self.kafka_registry_listener)
            location2 = (str(ip2), int(port2))
            result_of_check = a_socket2.connect_ex(location2)
            if result_of_check == 0: 
                registry_online = True
            else: 
                registry_online = False
            

            if broker_online != self.broker_online: changed = True
            if registry_online != self.registry_online: changed = True
                        
            self.subject_state = {'broker_online': broker_online, 'registry_online': registry_online}
            
            if changed: 
                self.__notify()

    def __check_connections(self): # Infinite loop that runs as a deamon thread to update the broker and registry status
        t = Thread(target=self.__check_conn_loop, args=(), daemon=True)
        t.start()
    
    @property
    def main_conf(self):
        if kConn.kafka_broker_listener is None: return ""

        ip, port = get_ip_and_port_from_string(kConn.kafka_broker_listener)
        formatted_address = f'{ip}:{port}'
        {'bootstrap.servers': formatted_address,}
    # END KAFKA CONNECTION ATTRIBUTES AND METHODS ///////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    # OBSERVER ATTRIBUTES AND METHODS ///////////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    def attach(self, observer): # Attcahes subscribers
        observer._subject = self
        self.__observers.add(observer)
        self.__notify()
        
    def detach(self, observer): # Detaches subscribers
        observer._subject = None
        self.__observers.discard(observer)
        
    def __notify(self): # Notifies subscribers of changes
        
        for observer in self.__observers:
            observer.update(self.subject_state)


    # PRODUCE RECORDS METHODS AND ATTRIBUTES ////////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @property
    def produce_queue(self):
        return self.__produce_queue

    @produce_queue.setter
    def produce_queue(self, value):
        self.__produce_queue = value

    @property
    def thread_count(self):
        return self._thread_count

    @thread_count.setter
    def thread_count(self, value):
        self._thread_count = value


    def __produce_record(self, thread_no, topic, value_schema_name, key_schema_name, values, keys, conf_):
        # print(f'Thread #{thread_no} is doing task #{task} in the queue.')
        #print(f'Trying task {topic} | {value_args} | {key_args} | {value_schema} | {key_schema}')

        prod = ProducerNative(conf_, value_schema_name, key_schema_name, thread_no)
        prod.produce(topic, values, keys)
        
        #print(f'Thread #{prod.tx_id} finished task #{thread_no} | {topic} | {value_args} | {key_args} | {value_schema} | {key_schema}')
        print(f'Thread #{prod.tx_id} finished task #{thread_no} | {topic} | {value_schema_name} | {key_schema_name}')


    def __start_producer_queue(self):
        '''
        queue_consumer is an infinite loop that runs only when the broker is connected.
            It then starts a specified number of thread (self.thread_count) that consumes the records that are placed 
            in the queue by instances of the Producers. These threads are passed the records to consume. 
            Once all threads are finished, it loops again.
        '''
        def __queue_consumer():        
            
            while True:        
            
                prods = []
                workers = []
                while self.broker_online:
                    
                    for i in range(self.thread_count):
                        task = self.produce_queue.get()
                        
                        topic, value_schema_name, key_schema_name, values, keys,  conf_ = task
                        prods.append(ProducerNative(conf_=conf_, value_schema_name=value_schema_name, key_schema_name=key_schema_name, tx_id=i))             
                        
                        worker = Thread(target=self.__produce_record, args=(i, topic, value_schema_name, key_schema_name, values, keys, conf_), daemon=False)
                        workers.append(worker)
                        worker.start()

                    for i in range(self.thread_count): 
                        workers[i].join()
                        
        queue_thread = Thread(target=__queue_consumer, args=(), daemon=True)
        queue_thread.start()
            
    # END PRODUCER RECORD METHODS AND ATTRIBUTES ////////////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# END CONNECTION CLASS //////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Create the Singleton instance
kConn = KafkaConnection()