import logging
import time
from typing import List, Optional, Union

import keyboard
import mouse

from . import common

logger = logging.getLogger(__name__)


class EventBase(common.Base):

    def play(self):
        raise NotImplementedError

    def __str__(self):
        return super().__repr__()


class KeyboardEvent(keyboard.KeyboardEvent, EventBase):

    def play(self):
        key = self.scan_code or self.name
        if self.event_type == keyboard.KEY_DOWN:
            keyboard.press(key)
        else:
            keyboard.release(key)


class ButtonEvent(EventBase):

    def __init__(self, event_type: str, button: str, time: float):
        self.event_type = event_type
        self.button = button
        self.time = time

    def play(self):
        if self.event_type == mouse.UP:
            mouse.release(self.button)
        else:
            mouse.press(self.button)


class MoveEvent(EventBase):

    def __init__(self, x: int, y: int, time: float):
        self.x = x
        self.y = y
        self.time = time

    def play(self):
        mouse.move(self.x, self.y)


class WheelEvent(EventBase):

    def __init__(self, delta: float, time: float):
        self.delta = delta
        self.time = time

    def play(self):
        mouse.wheel(self.delta)


MouseEvent = Union[MoveEvent, WheelEvent, ButtonEvent]
Event = Union[KeyboardEvent, MouseEvent]


class Recoder(common.Base):

    def __init__(self, name: str):
        self.name = name
        self.recording = False

    def _add_event(self, event: List[EventBase]):
        raise NotImplementedError

    def add_event(self, event: List[EventBase]):
        self._add_event(event)
        logger.debug(f"{self.name} olayı eklendi: {event}")

    def _record(self):
        controller = self.name.lower()
        if controller in ["mouse", "fare"]:
            mouse.hook(self.add_event)
        elif controller in ["keyboard", "klavye"]:
            keyboard.hook(self.add_event)
        else:
            raise ValueError(f"Hatalı değer: {controller} 'mouse' veya 'keyboard' olmalı")

    def _stop(self):
        controller = self.name.lower()
        if controller in ["mouse", "fare"]:
            mouse.unhook(self.add_event)
        elif controller in ["keyboard", "klavye"]:
            keyboard.unhook(self.add_event)
        else:
            raise ValueError(f"Hatalı değer: {controller} 'mouse' veya 'keyboard' olmalı")

    def record(self, append=False) -> bool:
        """Kaydı başlatır.
        Kayıt arkaplanda yapılır

        Returns:
            bool -- Kayıt başlatıldıysa `True`
        """
        if self.recording:
            logger.warning(f"{self.name} kaydı zaten yapılmakta")
            return False

        self._record()
        self.recording = True

        logger.info(f"{self.name} kaydı başlatıldı")
        return True

    def stop(self):
        """Kaydı durdurur

        Returns:
            bool -- Kayıt başlatıldıysa `True`
        """
        if not self.recording:
            logger.warning(f"{self.name} kaydı bulunamadı")
            return False

        self._stop()
        self.recording = False

        logger.info(f"{self.name} kaydı durduruldu")
        return True


class MouseRecorder(Recoder):

    def __init__(self):
        super().__init__("Fare")
        self.events: List[MouseEvent] = []

    def _add_event(self, event: MouseEvent):
        if isinstance(event, (ButtonEvent, MoveEvent, WheelEvent)):
            pass
        elif isinstance(event, mouse.MoveEvent):
            event = MoveEvent(
                event.x,
                event.y,
                event.time
            )
        elif isinstance(event, mouse.ButtonEvent):
            event = MoveEvent(
                event.event_type,
                event.button,
                event.time
            )
        elif isinstance(event, mouse.WheelEvent):
            event = MoveEvent(
                event.delta,
                event.time
            )
        else:
            raise ValueError(f"Olay tipi tanımlı değil: {type(event)}")

        self.events.append(event)


class KeyboardRecorder(Recoder):

    def __init__(self):
        super().__init__("Klavye")
        self.events: List[KeyboardEvent] = []

    def _add_event(self, event: KeyboardEvent):
        if isinstance(event, KeyboardEvent):
            pass
        if isinstance(event, keyboard.KeyboardEvent):
            event = KeyboardEvent(
                event.event_type,
                event.scan_code,
                event.name,
                event.time,
                event.device,
                event.modifiers,
                event.is_keypad
            )
        else:
            raise ValueError(f"Olay tipi tanımlı değil: {type(event)}")

        self.events.append(event)


class InputRecorder(Recoder):

    def __init__(self):
        """Girdi kayıt etme aracı
        """
        super().__init__("Girdi")

        self.mouse_recorder = MouseRecorder()
        self.keyboard_recorder = KeyboardRecorder()

    @property
    def events(self) -> List[Event]:
        events = self.mouse_recorder.events + self.keyboard_recorder.events
        events.sort(key=lambda x: x.time)
        return events

    @events.setter
    def events(self, events: List[Event]):
        mouse_events = []
        keyboard_events = []
        for event in events:
            if isinstance(event, (ButtonEvent, MoveEvent, WheelEvent)):
                mouse_events.append(event)
            elif isinstance(event, KeyboardEvent):
                keyboard_events.append(event)
            else:
                raise ValueError(f"Olay tipi tanımlı değil: {type(event)}")

        self.mouse_recorder.events = mouse_events
        self.keyboard_recorder.events = keyboard_events

    def _record(self):
        self.mouse_recorder._record()
        self.keyboard_recorder._record()

    def _stop(self):
        self.mouse_recorder._stop()
        self.keyboard_recorder._stop()

    def _add_event(self, event: Event):
        if isinstance(event, (ButtonEvent, MoveEvent, WheelEvent)):
            self.mouse_recorder.add_event(event)
        elif isinstance(event, KeyboardEvent):
            self.keyboard_recorder.add_event(event)
        else:
            raise ValueError(f"Olay tipi tanımlı değil: {type(event)}")

    def play(
        self,
        speed_factor=1.0,
        include_buttons=True,
        include_moves=True,
        include_wheels=True
    ) -> bool:
        """Tüm kayıtları oynatır
        Oynatma arkaplanda yapılmaz

        Keyword Arguments:
            speed_factor {float} -- Kayıtların oynatılma hızı (default: {1.0})
            include_buttons {bool} -- Mouse butonları dahil eder (default: {True})
            include_moves {bool} -- Mouse hareketlerini dahil elder (default: {True})
            include_wheel {bool} -- Mouse tekerleğini dahil eder (default: {True})

        Returns:
            bool -- Herhangi bir oynatma olduysa True
        """
        if not self.events:
            return False

        last_time: Optional[float] = None
        for event in self.events:
            if speed_factor > 0 and last_time:
                time.sleep((event.time - last_time) / speed_factor)
            last_time = event.time

            condition = any([
                isinstance(event, KeyboardEvent),
                include_buttons and isinstance(event, ButtonEvent),
                include_moves and isinstance(event, MoveEvent),
                include_wheels and isinstance(event, WheelEvent)
            ])

            if condition:
                event.play()

        return True
