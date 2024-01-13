from enum import Enum


class State(Enum):
    Created = 0
    Sent = 1
    Paid = 2
    NotPaid = 3
    Error = 4


def enum_encoder(enum_value):
    return enum_value.value


def enum_decoder(enum_cls, enum_value):
    return enum_cls(enum_value)
