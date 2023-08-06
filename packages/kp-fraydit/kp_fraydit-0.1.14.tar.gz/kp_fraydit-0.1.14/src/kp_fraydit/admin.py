from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import NewTopic

from kp_fraydit.connections.connection import KafkaConnection
from kp_fraydit.metaclasses import SingletonMeta


kConn = KafkaConnection()


class AdminEngine(AdminClient, metaclass=SingletonMeta):
    def __init__(self):
        # my_server = kConn.kafka_registry_listener.split("/")[2]
        ip, port = kConn.kafka_broker_listener.split(':')
        self.__conf = { "bootstrap.servers": f'{ip}:{port}' }
        super().__init__(self.__conf)

    def topic_exists(self, topic_name):
        topic_metadata = self.list_topics()
        if topic_metadata.topics.get(topic_name) is None: return False
        return True

    def create_topic(self, topic_name, num_partitions=5, retention_time=-1, retention_size=-1):
        if not self.topic_exists(topic_name):
            my_topic = NewTopic(topic=topic_name, num_partitions=5, config={'retention.ms': f'{retention_time}', 'retention.bytes': f'{retention_size}', })
            self.create_topics([my_topic,])
