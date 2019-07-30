from enum import Enum


class RoomStates(Enum):
    CLOSED = 0
    WAITING = 1
    RUNNING = 2
    PAUSED = 3
