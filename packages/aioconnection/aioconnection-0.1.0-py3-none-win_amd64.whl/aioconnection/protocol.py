from .utils import ftime

import asyncio
import time
import datetime
import typing as t
from enum import IntEnum
from collections import deque


class EventType(IntEnum):
    RECV = 0
    SEND = 1
    REPLY = 2
    CONNECTED = 3
    CONNECT_FAILED = 4
    IDLE = 5


# TODO добавить в инициализацию класса протокола
class Bytes(bytes):
    def __str__(self):
        return self.hex(bytes_per_sep=1, sep=' ')


class Event(t.NamedTuple):
    timestamp: t.Union[float, datetime.datetime, time.time]
    type: EventType
    data_raw: t.Optional[bytes]
    data: t.Optional[object]


# TODO Multiple transport on Protocol
class Protocol(asyncio.Protocol):
    DEBUG = False

    def __init__(self, *,
                 subscribers: t.Union[t.Callable, t.Iterable[t.Callable]] = None,
                 event_ftime: t.Callable = None,
                 idle_timeout: float = 0.0,
                 log_size: int = 0,
                 loop=None):
        self.log: t.Optional[deque[Event]] = deque(maxlen=log_size) if log_size else None
        self.transport: t.Optional[asyncio.Transport] = None

        self._subscribers = set()
        if subscribers:
            self.subscribe(subscribers)
        self._event_ftime = event_ftime or ftime
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._out_buffer = deque()
        self._allowed_to_write = False
        self._reply_awaiting = False
        self._reply_timeout_handle: t.Optional[asyncio.Handle] = None
        self._activity_last_time = 0.0
        self._idle_timeout = idle_timeout
        self._ping_task: t.Optional[asyncio.Task] = None
        self.__post_init__()

    def __post_init__(self, **kwargs):
        ...

    @property
    def idle_timeout(self):
        return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, timeout):
        self._idle_timeout = timeout
        if self._ping_task and not self._ping_task.done():
            self._ping_task.cancel()
        if timeout:
            self._ping_task = self._loop.create_task(self._pinging())

    async def _pinging(self):
        while True:
            await asyncio.sleep(self._idle_timeout)
            time_diff = ftime() - self._activity_last_time
            if time_diff >= self._idle_timeout and not (self._out_buffer or self._reply_timeout_handle):
                self._register_event(EventType.IDLE)

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        if self._idle_timeout:
            self._ping_task = self._loop.create_task(self._pinging())
        self._allowed_to_write = True
        self._write()
        if not (name := transport.get_extra_info('serialname')):
            name = transport.get_extra_info('peername')
            transport.set_write_buffer_limits(1, 1)
        self._register_event(EventType.CONNECTED, data=name)

    def connection_failed(self, exc=None, transport: asyncio.Transport = None):
        self.transport = transport or self.transport
        self._allowed_to_write = False
        self._ping_task and self._ping_task.cancel()
        self._register_event(EventType.CONNECT_FAILED, data=exc)

    def connection_lost(self, exc):
        self.connection_failed(exc)

    def parse_received_data(self, data_raw):
        yield data_raw, None

    def data_received(self, data_raw):
        self._activity_last_time = ftime()
        time_ = self._event_ftime()
        info_type = EventType.RECV
        if self._reply_timeout_handle:         # TODO do not send event if closing, except special reply callback
            self._reply_timeout_handle.cancel()
            self._reply_timeout_handle = None
            info_type = EventType.REPLY
            self._write()
        for data_raw, data in self.parse_received_data(data_raw):
            self._register_event(info_type, data_raw, data, time_)

    def resume_writing(self):
        self.data_drained()

    def pause_writing(self):
        self._allowed_to_write = False

    def data_drained(self):
        self._allowed_to_write = True
        data_raw, reply_timeout, data = self._out_buffer.popleft()
        if reply_timeout:
            self._reply_timeout_handle = self._loop.call_later(reply_timeout, self.data_received, None)
        else:
            self._write()
        self._register_event(EventType.SEND, data_raw, data)

    def write(self, data_raw, reply_timeout=0.0, data=None):
        self._out_buffer.append((data_raw, reply_timeout, data))
        self._write()

    def _write(self):
        if self._allowed_to_write and self._out_buffer and not self._reply_timeout_handle:
            try:
                self.transport.write(self._out_buffer[0][0])
            except RuntimeError:
                pass

    def _register_event(self, type_, data_raw=None, data=None, time_=None):
        time_ = time_ or self._event_ftime()
        event = Event(time_, type_, Bytes(data_raw or b''), data)
        if self.DEBUG:
            print(event)
        if self.log is not None and type_ is not EventType.IDLE:
            self.log.append(event)

        self._loop.call_soon(self.event_handler, event)
        for subscriber in self._subscribers:
            self._loop.call_soon(subscriber, event)

    def event_handler(self, event: Event = None):
        ...

    def subscribe(self, subscribers):
        if isinstance(subscribers, t.Iterable):
            self._subscribers.update(subscribers)
        else:
            self._subscribers.add(subscribers)

    def unsubscribe(self, subscribers):
        if isinstance(subscribers, t.Iterable):
            self._subscribers.difference_update(subscribers)
        else:
            try:
                self._subscribers.remove(subscribers)
            except KeyError:
                pass


if __name__ == '__main__':
    ...
