import time
from ...ypackage.model.input import InputRecorder


class TestInput:

    def test_input_recorder(self):
        inputRecorder = InputRecorder()

        assert inputRecorder.record()

        time.sleep(2)
        assert inputRecorder.stop()

        assert inputRecorder.events
