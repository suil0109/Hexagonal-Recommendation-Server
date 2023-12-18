from enum import Enum

UNUSED_REC_ID = -1
DOES_NOT_EXITS = -1

class Transaction(Enum):
    DEPOSIT = "deposit"
    DEDUCT = "deduct"

class Status(Enum):
    SUCCESS = "success"
    FAIL = "fail"
    WARNING = "warning"
    CAUTION = "caution"

class StatusCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_ERROR = 500
