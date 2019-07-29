from enum import Enum

LESSON_STATE_WAITING = "Wartet auf Beginn"


class RoomStates(Enum):
    CLOSED = 0
    WAITING = 1
    RUNNING = 2
    PAUSED = 3
