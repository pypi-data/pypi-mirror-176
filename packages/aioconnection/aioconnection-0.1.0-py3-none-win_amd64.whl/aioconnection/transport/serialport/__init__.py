from .core import (
    SerialSettings,
    StopBits,
    ByteSize,
    Parity,
    serialports_list
)

from .transport import SerialTransport

__all__ = ['SerialSettings',
           'StopBits',
           'ByteSize',
           'Parity',
           'serialports_list',
           'SerialTransport']