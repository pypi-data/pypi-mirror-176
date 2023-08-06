from abc import ABC

from kognic.io.model.input.abstract.base_frame import BaseFrame


class SequenceFrame(BaseFrame, ABC):
    frame_id: str
    relative_timestamp: int
