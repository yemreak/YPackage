
from ...ypackage.model.input import InputRecorder


class TestInput:

    def test_input_recorder(self):
        inputRecorder = InputRecorder()
        assert inputRecorder.record()
