from enum import Enum
from typing import NamedTuple, Optional, Union, List
from typing_extensions import TypedDict
from tim.types import Logs, Status


class BaseUnit(Enum):
  DAY = 'Day'
  HOUR = 'Hour'
  MINUTE = 'Minute'
  SECOND = 'Second'
  MONTH = 'Month'


class RelativeRange(TypedDict):
  baseUnit: BaseUnit
  value: int


class LatestVersion(TypedDict):
  id: str
  status: Status
  numberOfVariables: int
  numberOfObservations: int
  firstTimestamp: str
  lastTimestamp: str


class DatasetWorkspace(TypedDict):
  id: str
  name: str


class DatasetMetaData(TypedDict):
  id: str
  latestVersion: LatestVersion
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str
  description: str
  isFavorite: bool
  estimatedSamplingPeriod: str
  workspace: DatasetWorkspace
  name: str


class CSVSeparator(Enum):
  SEMICOLON = ';'
  TAB = ' '
  COMMA = ','


class UploadCSVConfiguration(TypedDict, total=False):
  timestampFormat: str
  timestampColumn: Union[str, int]
  csvSeparator: CSVSeparator
  name: str
  description: str
  samplingPeriod: RelativeRange
  workspaceId: str


class UploadCSVVersion(TypedDict):
  id: str


class UploadCsvResponse(TypedDict):
  id: str
  version: UploadCSVVersion


class UploadDatasetResponse(NamedTuple):
  id: str
  metaData: Optional[DatasetMetaData]
  logs: List[Logs]
