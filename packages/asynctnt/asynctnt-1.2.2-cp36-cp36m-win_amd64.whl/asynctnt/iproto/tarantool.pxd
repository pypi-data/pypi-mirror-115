cdef enum iproto_header_key:
    IPROTO_REQUEST_TYPE = 0x00
    IPROTO_SYNC = 0x01
    IPROTO_REPLICA_ID = 0x02
    IPROTO_LSN = 0x03
    IPROTO_TIMESTAMP = 0x04
    IPROTO_SCHEMA_VERSION = 0x05
    IPROTO_SERVER_VERSION = 0x06
    IPROTO_GROUP_ID = 0x07


cdef enum iproto_key:
    IPROTO_SPACE_ID = 0x10
    IPROTO_INDEX_ID = 0x11
    IPROTO_LIMIT = 0x12
    IPROTO_OFFSET = 0x13
    IPROTO_ITERATOR = 0x14
    IPROTO_INDEX_BASE = 0x15

    IPROTO_KEY = 0x20
    IPROTO_TUPLE = 0x21
    IPROTO_FUNCTION_NAME = 0x22
    IPROTO_USER_NAME = 0x23
    IPROTO_INSTANCE_UUID = 0x24
    IPROTO_CLUSTER_UUID = 0x25
    IPROTO_VCLOCK = 0x26
    IPROTO_EXPR = 0x27
    IPROTO_OPS = 0x28
    IPROTO_BALLOT = 0x29
    IPROTO_TUPLE_META = 0x2a
    IPROTO_OPTIONS = 0x2b

    IPROTO_DATA = 0x30
    IPROTO_ERROR = 0x31
    IPROTO_METADATA = 0x32

    IPROTO_SQL_TEXT = 0x40
    IPROTO_SQL_BIND = 0x41
    IPROTO_SQL_INFO = 0x42


cdef enum iproto_metadata_key:
    IPROTO_FIELD_NAME = 0
    IPROTO_FIELD_TYPE = 1


cdef enum iproto_sql_info_key:
    SQL_INFO_ROW_COUNT = 0
    SQL_INFO_AUTOINCREMENT_IDS = 1


cdef enum iproto_type:
    IPROTO_OK = 0
    IPROTO_SELECT = 1
    IPROTO_INSERT = 2
    IPROTO_REPLACE = 3
    IPROTO_UPDATE = 4
    IPROTO_DELETE = 5
    IPROTO_CALL_16 = 6
    IPROTO_AUTH = 7
    IPROTO_EVAL = 8
    IPROTO_UPSERT = 9
    IPROTO_CALL = 10
    IPROTO_EXECUTE = 11
    IPROTO_PING = 64

    IPROTO_CHUNK = 128

cdef enum iproto_update_operation:
    IPROTO_OP_ADD = b'+'
    IPROTO_OP_SUB = b'-'
    IPROTO_OP_AND = b'&'
    IPROTO_OP_XOR = b'^'
    IPROTO_OP_OR = b'|'
    IPROTO_OP_DELETE = b'#'
    IPROTO_OP_INSERT = b'!'
    IPROTO_OP_ASSIGN = b'='
    IPROTO_OP_SPLICE = b':'
