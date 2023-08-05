# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataSourceCreationInfo(Model):
    """DataSourceCreationInfo.

    :param content_hash:
    :type content_hash: str
    :param name:
    :type name: str
    :param data_type_id:
    :type data_type_id: str
    :param description:
    :type description: str
    :param data_store_name:
    :type data_store_name: str
    :param path_on_data_store:
    :type path_on_data_store: str
    :param sql_table_name:
    :type sql_table_name: str
    :param sql_query:
    :type sql_query: str
    :param sql_stored_procedure_name:
    :type sql_stored_procedure_name: str
    :param sql_stored_procedure_params:
    :type sql_stored_procedure_params:
     list[~swagger.models.StoredProcedureParameter]
    :param identifier_hash:
    :type identifier_hash: str
    """

    _attribute_map = {
        'content_hash': {'key': 'ContentHash', 'type': 'str'},
        'name': {'key': 'Name', 'type': 'str'},
        'data_type_id': {'key': 'DataTypeId', 'type': 'str'},
        'description': {'key': 'Description', 'type': 'str'},
        'data_store_name': {'key': 'DataStoreName', 'type': 'str'},
        'path_on_data_store': {'key': 'PathOnDataStore', 'type': 'str'},
        'sql_table_name': {'key': 'SqlTableName', 'type': 'str'},
        'sql_query': {'key': 'SqlQuery', 'type': 'str'},
        'sql_stored_procedure_name': {'key': 'SqlStoredProcedureName', 'type': 'str'},
        'sql_stored_procedure_params': {'key': 'SqlStoredProcedureParams', 'type': '[StoredProcedureParameter]'},
        'identifier_hash': {'key': 'IdentifierHash', 'type': 'str'},
    }

    def __init__(self, content_hash=None, name=None, data_type_id=None, description=None, data_store_name=None, path_on_data_store=None, sql_table_name=None, sql_query=None, sql_stored_procedure_name=None, sql_stored_procedure_params=None, identifier_hash=None):
        super(DataSourceCreationInfo, self).__init__()
        self.content_hash = content_hash
        self.name = name
        self.data_type_id = data_type_id
        self.description = description
        self.data_store_name = data_store_name
        self.path_on_data_store = path_on_data_store
        self.sql_table_name = sql_table_name
        self.sql_query = sql_query
        self.sql_stored_procedure_name = sql_stored_procedure_name
        self.sql_stored_procedure_params = sql_stored_procedure_params
        self.identifier_hash = identifier_hash
