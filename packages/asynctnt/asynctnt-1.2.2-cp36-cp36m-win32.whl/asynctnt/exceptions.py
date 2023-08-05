import enum


class TarantoolError(Exception):
    """
        Base Tarantool Exception class
    """
    pass


class TarantoolSchemaError(TarantoolError):
    """
        Exception is raised when any problems with schema occurred
    """
    pass


class TarantoolDatabaseError(TarantoolError):
    """
        Exception is raised when Tarantool responds with code != 0
    """
    def __init__(self, code, message):
        super(TarantoolDatabaseError, self).__init__(code, message)
        self.code = code
        self.message = message


class TarantoolNetworkError(TarantoolError):
    pass


class TarantoolNotConnectedError(TarantoolNetworkError):
    """
        Raised when asynctnt is not connected to Tarantool
    """
    pass


class ErrorCode(enum.IntEnum):
    """
        Tarantool default error codes
    """
    ER_UNKNOWN = 0
    ER_ILLEGAL_PARAMS = 1
    ER_MEMORY_ISSUE = 2
    ER_TUPLE_FOUND = 3
    ER_TUPLE_NOT_FOUND = 4
    ER_UNSUPPORTED = 5
    ER_NONMASTER = 6
    ER_READONLY = 7
    ER_INJECTION = 8
    ER_CREATE_SPACE = 9
    ER_SPACE_EXISTS = 10
    ER_DROP_SPACE = 11
    ER_ALTER_SPACE = 12
    ER_INDEX_TYPE = 13
    ER_MODIFY_INDEX = 14
    ER_LAST_DROP = 15
    ER_TUPLE_FORMAT_LIMIT = 16
    ER_DROP_PRIMARY_KEY = 17
    ER_KEY_PART_TYPE = 18
    ER_EXACT_MATCH = 19
    ER_INVALID_MSGPACK = 20
    ER_PROC_RET = 21
    ER_TUPLE_NOT_ARRAY = 22
    ER_FIELD_TYPE = 23
    ER_FIELD_TYPE_MISMATCH = 24
    ER_SPLICE = 25
    ER_ARG_TYPE = 26
    ER_TUPLE_IS_TOO_LONG = 27
    ER_UNKNOWN_UPDATE_OP = 28
    ER_UPDATE_FIELD = 29
    ER_FIBER_STACK = 30
    ER_KEY_PART_COUNT = 31
    ER_PROC_LUA = 32
    ER_NO_SUCH_PROC = 33
    ER_NO_SUCH_TRIGGER = 34
    ER_NO_SUCH_INDEX = 35
    ER_NO_SUCH_SPACE = 36
    ER_NO_SUCH_FIELD = 37
    ER_EXACT_FIELD_COUNT = 38
    ER_INDEX_FIELD_COUNT = 39
    ER_WAL_IO = 40
    ER_MORE_THAN_ONE_TUPLE = 41
    ER_ACCESS_DENIED = 42
    ER_CREATE_USER = 43
    ER_DROP_USER = 44
    ER_NO_SUCH_USER = 45
    ER_USER_EXISTS = 46
    ER_PASSWORD_MISMATCH = 47
    ER_UNKNOWN_REQUEST_TYPE = 48
    ER_UNKNOWN_SCHEMA_OBJECT = 49
    ER_CREATE_FUNCTION = 50
    ER_NO_SUCH_FUNCTION = 51
    ER_FUNCTION_EXISTS = 52
    ER_FUNCTION_ACCESS_DENIED = 53
    ER_FUNCTION_MAX = 54
    ER_SPACE_ACCESS_DENIED = 55
    ER_USER_MAX = 56
    ER_NO_SUCH_ENGINE = 57
    ER_RELOAD_CFG = 58
    ER_CFG = 59
    ER_VINYL = 60
    ER_LOCAL_SERVER_IS_NOT_ACTIVE = 61
    ER_UNKNOWN_SERVER = 62
    ER_CLUSTER_ID_MISMATCH = 63
    ER_INVALID_UUID = 64
    ER_CLUSTER_ID_IS_RO = 65
    ER_SERVER_ID_MISMATCH = 66
    ER_SERVER_ID_IS_RESERVED = 67
    ER_INVALID_ORDER = 68
    ER_MISSING_REQUEST_FIELD = 69
    ER_IDENTIFIER = 70
    ER_DROP_FUNCTION = 71
    ER_ITERATOR_TYPE = 72
    ER_REPLICA_MAX = 73
    ER_INVALID_XLOG = 74
    ER_INVALID_XLOG_NAME = 75
    ER_INVALID_XLOG_ORDER = 76
    ER_NO_CONNECTION = 77
    ER_TIMEOUT = 78
    ER_ACTIVE_TRANSACTION = 79
    ER_NO_ACTIVE_TRANSACTION = 80
    ER_CROSS_ENGINE_TRANSACTION = 81
    ER_NO_SUCH_ROLE = 82
    ER_ROLE_EXISTS = 83
    ER_CREATE_ROLE = 84
    ER_INDEX_EXISTS = 85
    ER_TUPLE_REF_OVERFLOW = 86
    ER_ROLE_LOOP = 87
    ER_GRANT = 88
    ER_PRIV_GRANTED = 89
    ER_ROLE_GRANTED = 90
    ER_PRIV_NOT_GRANTED = 91
    ER_ROLE_NOT_GRANTED = 92
    ER_MISSING_SNAPSHOT = 93
    ER_CANT_UPDATE_PRIMARY_KEY = 94
    ER_UPDATE_INTEGER_OVERFLOW = 95
    ER_GUEST_USER_PASSWORD = 96
    ER_TRANSACTION_CONFLICT = 97
    ER_UNSUPPORTED_ROLE_PRIV = 98
    ER_LOAD_FUNCTION = 99
    ER_FUNCTION_LANGUAGE = 100
    ER_RTREE_RECT = 101
    ER_PROC_C = 102
    ER_UNKNOWN_RTREE_INDEX_DISTANCE_TYPE = 103
    ER_PROTOCOL = 104
    ER_UPSERT_UNIQUE_SECONDARY_KEY = 105
    ER_WRONG_INDEX_RECORD = 106
    ER_WRONG_INDEX_PARTS = 107
    ER_WRONG_INDEX_OPTIONS = 108
    ER_WRONG_SCHEMA_VERSION = 109
    ER_SLAB_ALLOC_MAX = 110
    ER_WRONG_SPACE_OPTIONS = 111
    ER_UNSUPPORTED_INDEX_FEATURE = 112
    ER_VIEW_IS_RO = 113
    ER_SERVER_UUID_MISMATCH = 114
    ER_SYSTEM = 115
    ER_LOADING = 116
    ER_CONNECTION_TO_SELF = 117
    ER_KEY_PART_IS_TOO_LONG = 118
    ER_COMPRESSION = 119
