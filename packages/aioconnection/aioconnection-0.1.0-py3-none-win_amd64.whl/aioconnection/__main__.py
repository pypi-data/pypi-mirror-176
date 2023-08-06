from aioconnection import *
from aioconnection.transport.serialport import *

import asyncio
import typing as t


class LedsArduino(Protocol):
    DEBUG = True
    SCHEMA_DICT = {'R': 256 * 256, 'G': 256, 'B': 1}

    def __init__(self, *,
                 subscribers: t.Union[t.Callable, t.Iterable[t.Callable]] = None,
                 event_ftime: t.Callable = None,
                 idle_timeout=0.0,
                 log_size=0,
                 loop=None):
        super().__init__(subscribers=subscribers, idle_timeout=idle_timeout, event_ftime=event_ftime,
                         log_size=log_size, loop=loop)
        schema = 'GRB'
        self.factors = [self.SCHEMA_DICT.get(color_name) for color_name in schema]
        self.led_count = 80
        self.init_passed = False
        self.leds_current_state = [None] * self.led_count
        self.test_leds_task: t.Optional[asyncio.Task] = None

    def event_handler(self, event: Event = None):
        if event.type is EventType.CONNECT_FAILED:
            print(isinstance(event.data, Exception))
        if event.type in (EventType.RECV, EventType.REPLY):
            ...
        elif event.type is EventType.CONNECTED:
            if not self.init_passed:
                self.init(self.led_count, (0, 0, 0))
                self.init_passed = True

    def _rgb_to_int(self, rgb_color: t.Union[tuple, list]):
        return sum(factor * color for factor, color in zip(self.factors, rgb_color))

    def init(self, count: int, color: t.Union[tuple, list]):
        self.write('LEDs::init {0:d} {1:x};'.format(count, self._rgb_to_int(color)).encode(), reply_timeout=0.2)

    def set_color(self, index: int, color: t.Union[tuple, list]):
        self.leds_current_state[index] = color
        self._set_color(index, color)

    def _set_color(self, index: int, color: t.Union[tuple, list]):
        self.write('LEDs::setColor {0:d} {1:x};'.format(index, self._rgb_to_int(color)).encode(), reply_timeout=0.2)

    def restore_state(self):
        black = (0, 0, 0)
        self.init(self.led_count, black)
        for index, color in enumerate(self.leds_current_state):
            if color and color != black:
                self._set_color(index, color)

    def test_leds(self, active):
        if active:
            if self.test_leds_task is None or self.test_leds_task.done():
                self.test_leds_task = self._loop.create_task(self._test_leds())
        else:
            if self.test_leds_task and not self.test_leds_task.done():
                self.test_leds_task.cancel()
                self.restore_state()

    async def _test_leds(self):
        while True:
            for color in ((10, 0, 0), (0, 10, 0), (0, 0, 10)):
                if not self._out_buffer:
                    self.init(self.led_count, color)
                await asyncio.sleep(0.3)



if __name__ == '__main__':

    async def aio_main():
        port = 'COM51'
        leds = LedsArduino(idle_timeout=0)
        SerialTransport(leds, port, SerialSettings(baudrate=9600, parity=Parity.NONE, silence=10))
        await asyncio.sleep(0.2)
        colors = [(10, 0, 0), (10, 10, 0), (0, 10, 0), (0, 10, 10), (0, 0, 10), ] * 10
        stage = -1
        step = [0] * 3
        current_color = colors[0]
        for index in range(80):
            print(index)
            if current_color == colors[stage + 1]:
                stage += 1
                step = [int((next_ - current) / 5) for current, next_ in zip(current_color, colors[stage + 1])]
            current_color = tuple(current + stp for current, stp in zip(current_color, step))
            leds.set_color(index, current_color)
        while True:
            await asyncio.sleep(10)

    asyncio.run(aio_main())
