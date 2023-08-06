import json
import os
import sys

from kp_fraydit.connectors.connector import Connector
from kp_fraydit.schema_client import SchemaEngine
from kp_fraydit.admin import AdminEngine


# conf = {'bootstrap.servers': formatted_address,}
eng = SchemaEngine()
admin = AdminEngine()


class PriceConnector(Connector):
    def __init__(self, source_name):
        super().__init__(source_name)
        
        self.__source_name = source_name
        self.__value_schema_name = f'{source_name}-value'
        self.__key_schema_name = f'{source_name}-key'
        
        # Validate the schemas
        root_dir = print(sys.path[1])
        file_handler = logging.FileHandler(f'{root_dir}/logs/errors_{today_as_string()}.log')

        eng.validate_schema(self.__source_name, self.__value_schema_name, f'{root_dir}/schemas/price_data_value.avro')
        eng.validate_schema(self.__source_name, self.__key_schema_name, f'{root_dir}/schemas/price_data_key.avro')


    @property
    def source_name(self):
        return self.__source_name

    @property
    def value_schema_name(self):
        return self.__value_schema_name

    @property
    def key_schema_name(self):
        return self.__key_schema_name

    def create_schema(self, schema_dict):
        pass