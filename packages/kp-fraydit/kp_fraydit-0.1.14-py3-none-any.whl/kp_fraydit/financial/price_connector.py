import json
import os
import sys

from kp_fraydit.connectors.connector import Connector
from kp_fraydit.schema_client import SchemaEngine
from kp_fraydit.admin import AdminEngine
from kp_fraydit.root import root_dir


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
        
        eng.validate_schema(self.__source_name, self.__value_schema_name, f'https://fraydit.com/static/schemas/price_data_value.txt')
        eng.validate_schema(self.__source_name, self.__key_schema_name, f'https://fraydit.com/static/schemas/price_data_key.txt')


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
