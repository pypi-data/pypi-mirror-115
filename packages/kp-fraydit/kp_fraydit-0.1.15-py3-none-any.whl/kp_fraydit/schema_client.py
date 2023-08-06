import os
import json
import requests


from confluent_kafka.admin import NewTopic
from confluent_kafka.admin import AdminClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry import Schema

from kp_fraydit.connections.connection import KafkaConnection
from kp_fraydit.metaclasses import SingletonMeta
from .custom_errors import CustomError, RegistryOfflineError


kConn = KafkaConnection()
schema_compatibility_modes = ['FULL_TRANSITIVE', 'FULL', 'FORWARD_TRANSITIVE', 'FORWARD', 'BACKWARD', 'BACKWARD_TRANSITIVE', 'NONE']


class SchemaEngine(SchemaRegistryClient, metaclass=SingletonMeta):

    def __init__(self):
        #with ConnectionSettings() as conn:
        try:
            if not kConn.registry_online: raise RegistryOfflineError
            schema_client_conf = {'url':f'{kConn.kafka_registry_listener}'}
            self._schema_client = SchemaRegistryClient(schema_client_conf)
            super().__init__(schema_client_conf)
        
        except RegistryOfflineError as e:
            pass
        
        except Exception as e:
            raise CustomError(e)
    
    @property
    def schema_subjects(self):
        return self.get_subjects()

    
    def get_latest_schema(self, schema_subject):
        try:
            return super().get_latest_version(schema_subject).schema
        except:
            return None

    
    # GET VALUE FIELDS //////////////////////////////////////////////////////////////////////////////////////////////////
    
    '''
    Helper function that processes the schema type and sets the required, optional, and all fields for the value schema.
    This function flattens a nested Avro schema and that allows for nesting capabilities. This only works for Avro schema.
    The nested schema needs to be like this:
    fields: [
        {
            "name": "nestedField",
            "type": [
                {
                    "doc": "struture that contains nested info",
                    "name": "TestpathElement",
                    "namespace": "com.example.kafka.core",
                    "type": "record"
                    "fields": [
                        {
                            "name": "sourceNested",
                            "type": "string"
                        },
                        {
                            "name": "timestampNested",
                            "type": "long"
                        }
                    ],
                }
            ]
        }
    ]
    '''
    def get_value_fields(self, **kwargs):
        if 'schema_name' in kwargs: current_value_schema = self.get_latest_schema(kwargs.get('schema_name'))
        else: current_value_schema = kwargs.get('schema')
        value_fields = []
        all_fields = []
        required_value_fields = []
        optional_value_fields = []

    
        if current_value_schema is None:     # No schema
            value_dict = dict()
            value_dict['name'] = 'value'
            value_dict['type'] = ['string', 'float']
            value_fields = [value_dict]
            all_fields.append(value_dict)
            required_value_fields.append(value_dict)
            return {
                'value_fields': all_fields,
                'required_value_fields': required_value_fields,
                'optional_value_fields': optional_value_fields
            }

        if current_value_schema.schema_type == 'AVRO': # Avro schema
            value_fields = eval('dict('+current_value_schema.schema_str+')')['fields']
            
        elif current_value_schema.schema_type == 'JSON': # JSON schema

            json_list = []
            value_fields = eval('dict('+current_value_schema.schema_str+')')['properties']
            for value_field_name, value_field_contents in value_fields.items():
                my_dict = {}
                my_dict['name'] = value_field_name
                for k, v in value_field_contents.items():
                    if k == 'description': my_dict['doc'] = v
                    else: my_dict[k] = v
                    
                json_list.append(my_dict)
            value_fields = json_list
        
        for value_field in value_fields:
            
            required = True
            nested = False
            if isinstance(value_field['type'], list): # the type is a list
                if 'null' in value_field['type']: required = False # check for null
                # print (value_field['type'])    
                for type_ in value_field['type']: # iterate the type
                    nested = False
                    # Check for nested elements
                    if isinstance(type_, dict): # Dictionary of elements. 
                        nested = True # toggle nested for the purposes of adding the fields
                        if 'type' in type_.keys(): # type exists in dictionary
                            
                            if type_['type'] == 'record': # type is array. Get the fields from the items key
                                for element in type_['fields']: # iterate the sub elements
                                    subtype_required = True # toggle on required for subtype
                                    element['record'] = type_['name'] # add the parent
                                    element['parent'] = value_field['name']
                                    # Add the field to all fields
                                    all_fields.append(element)
                                    # Add the field to either required or optional
                                    if isinstance(element['type'], list):
                                        
                                        for subtype_ in element['type']: # iterate type that is list
                                            if subtype_ == 'null': subtype_required = False
                                    else:
                                        if element['type'] == 'null': subtype_required = False
                                    # Set if optional or required
                                    if subtype_required and required: required_value_fields.append(element)
                                    else: optional_value_fields.append(element)
                        else: # the type is a list. there is a dictionary in the type. type does not exist in in the keys
                            pass
                    else: # the type is a list. there is a dictionary in the type
                        pass

            else: # the type is not a list. It is not nested
                if value_field == 'null': required = False
            
            if not nested:
                all_fields.append(value_field)
                if required: required_value_fields.append(value_field)
                else: optional_value_fields.append(value_field)
    
        return {
            'value_fields': all_fields,
            'required_value_fields': required_value_fields,
            'optional_value_fields': optional_value_fields
        }

    # END GET VALUE FIELDS //////////////////////////////////////////////////////////////////////////////////////////////


    # GET KEY FIELDS ////////////////////////////////////////////////////////////////////////////////////////////////////

    def get_key_fields(self, **kwargs):
        if 'schema_name' in kwargs: current_key_schema = self.get_latest_schema(kwargs.get('schema_name'))
        else: current_key_schema = kwargs.get('schema')

        
        # current_key_schema = schema
        key_fields = []
        all_fields = []
        required_key_fields = []
        optional_key_fields = []

        # Return value for no key
        if current_key_schema is None:
            key_dict = dict()
            key_dict['name'] = 'key'
            key_dict['type'] = ['null', 'string']
            key_fields = [key_dict]
            all_fields.append(key_dict)
            optional_key_fields.append(key_dict)
            return {
                'key_fields': all_fields,
                'required_key_fields': required_key_fields,
                'optional_key_fields': optional_key_fields
            }

        # process avro schema
        elif current_key_schema.schema_type == 'AVRO': 
            key_fields = eval('dict('+current_key_schema.schema_str+')')['fields']

        # process json schema
        elif current_key_schema.schema_type == 'JSON': 

            json_list = []
            key_fields = eval('dict('+current_key_schema.schema_str+')')['properties']
            for key_field_name, key_field_contents in key_fields.items():
                my_dict = {}
                my_dict['name'] = key_field_name
                for k, v in key_field_contents.items():
                    if k == 'description': my_dict['doc'] = v
                    else: my_dict[k] = v
                    
                json_list.append(my_dict)
            key_fields = json_list

        """
        The key fields have been processed according to the schema. 
        """
        all_fields = []

        for key_field in key_fields:

            all_fields.append(key_field)
            
            not_required = False
            if type(key_field['type']) is list:
                for type_ in key_field['type']:
                    if type_ == 'null': not_required = True
            else: 
                if key_field == 'null': not_required = True

            if not_required: optional_key_fields.append(key_field)
            else: required_key_fields.append(key_field)

        return {
            'key_fields': all_fields,
            'required_key_fields': required_key_fields,
            'optional_key_fields': optional_key_fields
        }

    # END GET KEY FIELDS //////////////////////////////////////////////////////////////////////////////////////////////

    def get_field_names(self, list_):
        
        if not isinstance(list_, list): return []
        my_list = list()
        for field in list_:
            
            my_list.append(field['name'])
        return my_list

    
    def schema_exists(self, schema_name):
        try:
            value = self.get_latest_schema(schema_name)

            if value is None: return False
        except:
            return False

        return True


    def validate_schema(self, subject_name, schema_name, base_schema_source):

        # VALIDATE VALUE SCHEMA ////////////////////////////////////////////////

        # Load the json data structure
        r = requests.get(base_schema_source)
        data = r.json()
        base_value_fields = data['fields']
        base_value_field_names = self.get_field_names(base_value_fields)


        # set the head of the schema
        new_schema_dict = {}
        new_schema_dict['type'] = data['type']
        schema_namespace = f'{data["namespace"]}.{subject_name}'
        new_schema_dict['namespace'] = schema_namespace
        new_schema_dict['doc'] = data['doc']
        new_schema_dict['name'] = subject_name

        if self.schema_exists(schema_name):
            current_schema = self.get_latest_schema(schema_name)
            current_schema_dict = json.loads(current_schema.schema_str)
            

            values = self.get_value_fields(schema=current_schema)
            new_values = values['value_fields']
            
            # Validate that the existing fields are good
            for field in new_values:
                if field['name'] in base_value_field_names:
                    # Get the base field
                    base_field = [f for f in base_value_fields if f['name'] == field['name']][0]
                    
                    # Check the field attributes and make sure they are identical. If not, delete the field
                    for key, value in field.items():
                        if not base_field.get(key) == value:
                            new_values.remove(field)
                            break

            # Add fields that are missing
            print (set(base_value_field_names))
            print (set(self.get_field_names(new_values)))
            missing_value_fields = set(base_value_field_names) - set(self.get_field_names(new_values))
            print (f'Missing fields: {missing_value_fields}')
            
            # Count missing fields. If none, exit with no change
            if not len(missing_value_fields):
                return False

            for field in missing_value_fields:
                field_dict = [d for d in base_value_fields if d['name'] == field]
                new_values.append(field_dict[0])
            
            
            new_schema_dict['fields'] = new_values

        else: # Create a schema from base
            print ('Creating new schema')
            new_schema_dict = data
            new_schema_dict['namespace'] = schema_namespace
        

        # Format namespace and create the new Schema object
        new_schema_dict['namespace'] = f'{schema_namespace}' # Set namespace from previous value
        formatted_schema_str = str(new_schema_dict).replace("'", '"') # replace single quotes with double quotes
        # formatted_schema_str = str(new_schema_dict)
        new_schema = Schema(schema_str=str(formatted_schema_str),schema_type='AVRO')

        # Try to update the schema. On Failure, iterate through compatiblity modes and try to change
        while True:
            try:
                # Register the schema
                self.register_schema(schema_name, new_schema)
                return True
            except:
                pass
                # print ('failed')
            
            for count, comp in enumerate(schema_compatibility_modes):
                try:
                    print (f'Compare: {comp} Count: {count}')
                    self.set_compatibility(schema_name, level=comp)
                    # Register the schema
                    self.register_schema(schema_name, new_schema)
                    return True
                except:
                    if count == len(schema_compatibility_modes): return False

