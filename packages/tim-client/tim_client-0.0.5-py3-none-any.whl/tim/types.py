from enum import Enum
from typing_extensions import TypedDict


class Origin(Enum):
  REGISTRATION = 'Registration'
  EXECUTION = 'Executed'
  VALIDATION = 'Validation'


class MessageType(Enum):
  INFO = 'Info'
  WARNING = 'Warning'
  ERROR = 'Error'


class Logs(TypedDict):
  createdAt: str
  origin: Origin
  message: str
  messageType: MessageType


class Status(Enum):
  REGISTERED = 'Registered'
  RUNNING = 'Running'
  FINISHED = 'Finished'
  FINISHED_WITH_WARNING = 'FinishedWithWarning'
  FAILED = 'Failed'
  QUEUED = 'Queued'


class StatusResponse(TypedDict):
  createdAt: str
  status: Status
  progress: float
  memory: int
  CPU: int
