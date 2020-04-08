import logging
import time
from typing import Callable, List, Union

import keyboard
import mouse

from ..core import background
from . import common

logger = logging.getLogger(__name__)


class Event(common.Base):

    def play(self):
        raise NotImplementedError


class KeyboardEvent(keyboard.KeyboardEvent, Event):

    def play(self):
        key = self.scan_code or self.name
        if self.event_type == keyboard.KEY_DOWN:
            keyboard.press(key)
        else:
            keyboard.release(key)


class ButtonEvent(Event):

    def __init__(self, button_event: mouse.ButtonEvent):
        self.event_type = button_event.event_type
        self.button = button_event.button
        self.time = button_event.time

    def play(self):
        if self.event_type == mouse.UP:
            mouse.release(self.button)
        else:
            mouse.press(self.button)


class MoveEvent(Event):

    def __init__(self, button_event: mouse.MoveEvent):
        self.x = button_event.x
        self.y = button_event.y
        self.time = button_event.time

    def play(self):
        mouse.move(self.event.x, self.event.y)


class WheelEvent(Event):

    def __init__(self, button_event: mouse.WheelEvent):
        self.delta = button_event.delta
        self.time = button_event.time

    def play(self):
        mouse.wheel(self.event.delta)


class InputEvent(Event):

    def __init__(self, event: Union[
        KeyboardEvent,
        ButtonEvent,
        WheelEvent,
        MoveEvent
    ]):
        self.event = event
        self.last_time = None

    def play(
        self,
        speed_factor=1.0,
        include_clicks=True,
        include_moves=True,
        include_wheel=True
    ):
        if speed_factor > 0 and self.last_time is not None:
            time.sleep((self.event.time - self.last_time) / speed_factor)
        self.last_time = self.event.time

        condition = any([
            isinstance(self.event, keyboard.KeyboardEvent),
            isinstance(self.event, mouse.ButtonEvent) and include_clicks,
            isinstance(self.event, mouse.MoveEvent) and include_moves,
            isinstance(self.event, mouse.WheelEvent) and include_wheel
        ])

        if condition:
            self.event.play()


class Recoder(common.Base):

    @background.do_background
    @staticmethod
    def record_custom(controller: str, hook: Callable[[Event], None]):
        if controller == "mouse":
            mouse.hook(hook)
        elif controller == "keyboard":
            keyboard.hook(hook)
        else:
            raise ValueError("Hatalı değer: 'mouse' veya 'keyboard' olmalı")

    @staticmethod
    def stop_custom(controller: str, hook: Callable[[Event], None]):
        if controller == "mouse":
            mouse.unhook(hook)
        elif controller == "keyboard":
            keyboard.unhook(hook)
        else:
            raise ValueError("Hatalı değer: 'mouse' veya 'keyboard' olmalı")

    def __init__(self, name: str):
        self.name = name

        self.events: List[Event] = []
        self.recording = False

    def _add_event(self, event: List[Event]):
        self.events.append(event)

    def add_event(self, event: List[Event]):
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
        elif controller == ["keyboard", "klavye"]:
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

    # TODO: Bu yapıyı diğerlerine de uygula
    def __init__(self):
        super().__init__("Fare")

    def _add_event(self, event: Union[MoveEvent, WheelEvent, ButtonEvent]):
        return self._add_event(event)


class KeyboardRecorder(Recoder):

    def __init__(self):
        super().__init__("Klavye")

    def _add_event(self, event: KeyboardEvent):
        return self._add_event(event)


class InputRecorder(Recoder):

    def __init__(self):
        """Girdi kayıt etme aracı
        """
        super().__init__("Girdi")

        self.mouse_recorder = MouseRecorder()
        self.keyboard_recorder = KeyboardRecorder()

    def _record(self):
        self.mouse_recorder._record()
        self.keyboard_recorder._record()

    def _stop(self):
        self.mouse_recorder._stop()
        self.keyboard_recorder._stop()

    def _store_events(self):
        _events = self.mouse_recorder.events + self.keyboard_recorder.events
        _events = _events.sort(key=lambda x: x.time)
        self.events = [InputEvent(_event) for _event in _events]

    def stop(self) -> bool:
        """Klavye ve mouse kaydını durdurur

        Returns:
            bool -- Kayıt başlatıldıysa `True`
        """
        if not super().stop():
            return False

        self._store_events()
        logger.info("Kaydedilen olaylar işlendi")

        return True

    def play(self, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
        """Tüm kayıtları oynatır
        Oynatma arkaplanda yapılmaz

        Keyword Arguments:
            speed_factor {float} -- Kayıtların oynatılma hızı (default: {1.0})
            include_clicks {bool} -- Tıklamaları dahil eder (default: {True})
            include_moves {bool} -- Mouse hareketlerini dahil elder (default: {True})
            include_wheel {bool} -- Mouse tekerleğini dahil eder (default: {True})
        """
        for event in self.events:
            event.play()
