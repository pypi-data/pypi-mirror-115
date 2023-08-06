from kp_fraydit.producers.producer import Producer
from kp_fraydit.schema_client import SchemaEngine

class LogProducer(Producer):
    def __init__(self):

        # Create the topic if not found
        seng = SchemaEngine()
        try:
            seng.get_latest_schema('logger')
        except:
            attempts = 0
            while True:
                if seng.create_topic: break
                if attempts == 10:
                    raise
            
            # Create the schema
            key_schema = ''
            value_schema = ''
            seng.register_schema('logger', key_schema)

        

        super().__init__('logger')