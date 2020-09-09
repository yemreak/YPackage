import time

import keyboard
import mouse
import pytest

from ...ypackage.model.input import (
    ButtonEvent, InputRecorder, KeyboardEvent, MoveEvent, WheelEvent)


class TestInputRecorder:

    @pytest.fixture(autouse=True)
    def init_recorder(self):
        self.recorder = InputRecorder()

    def test_recoder_controls(self):
        return
        assert self.recorder.record()
        assert self.recorder.stop()
        assert not self.recorder.events

    def test_add_event(self):
        firsttime = time.time()
        secondtime = time.time()

        events = [
            MoveEvent(1, 2, firsttime),
            MoveEvent(1, 5, secondtime)
        ]

        for event in events:
            self.recorder.add_event(event)

        assert self.recorder.events == events

    def test_add_record(self):
        curtime = time.time()
        events = [
            MoveEvent(1, 2, curtime),
            KeyboardEvent(keyboard.KEY_UP, "a", time=curtime - 0.25),
            WheelEvent(1, curtime - 0.5),
            ButtonEvent(1, 2, curtime - 0.75)
        ]

        for event in events:
            self.recorder.add_event(event)
        assert self.recorder.events == events[::-1]

        self.recorder.events = []
        assert not self.recorder.events

        self.recorder.events = events
        assert self.recorder.events == events[::-1]

    def test_play_records(self):
        return
        curtime = time.time()

        events = [
            MoveEvent(200, 40, curtime),
            KeyboardEvent(keyboard.KEY_DOWN, "a", time=curtime + 0.1),
            KeyboardEvent(keyboard.KEY_UP, "a", time=curtime + 0.25),
            WheelEvent(-50, curtime + 0.5),
            ButtonEvent(mouse.DOWN, mouse.LEFT, curtime + 0.75),
            ButtonEvent(mouse.UP, mouse.LEFT, curtime + 0.85)
        ]
        self.recorder.events = events
        self.recorder.play()

        # Segmentation fault on Circle CI
        # assert (200, 40) == mouse.get_position()

    def test_wrong_event(self):
        with pytest.raises(ValueError):
            self.recorder.events = "YPackage"

        with pytest.raises(ValueError):
            self.recorder.add_event("YEmreAk")
