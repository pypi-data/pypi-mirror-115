import json

from kp_fraydit.admin import AdminEngine
from kp_fraydit.connections.connection import KafkaConnection
from kp_fraydit.producers.producer import Producer
from kp_fraydit.schema_client import SchemaEngine


eng = SchemaEngine()
admin = AdminEngine()
kConn = KafkaConnection()

default_topic_creation_conf = {
    'num_partitions': '5',
    'retention_time': '-1',
    'retention_size': '-1',
}

class Connector:
    def __init__(self, source_name, topic_creation_conf=default_topic_creation_conf):
        self.__source_name = source_name

        # Check to see if the topic exists
        if not admin.topic_exists(source_name): admin.create_topic(topic_name=source_name, num_partitions=topic_creation_conf['num_partitions'], retention_time=topic_creation_conf['retention_time'], retention_size=topic_creation_conf['retention_size'])
        self.__producer = Producer(source_name)
        # self.consumer = consumer
        

    @property
    def source_name(self):
        return self.__source_name


    @property
    def producer(self):
        return self.__producer

    

