from io import StringIO
import pandas as pd
from typing import List
from time import sleep
from tim.types import Logs, Status, StatusResponse
from tim.core.api import execute_request
from tim.data_sources.anomaly_detection.types import AnomalyDetectionJobModelResult, AnomalyDetectionMetaData, BuildModelResponse, AnomalyDetectionJobConfiguration, ExecuteResponse
from tim.core.credentials import Credentials


def build_model(
    credentials: Credentials, job_configuration: AnomalyDetectionJobConfiguration
) -> BuildModelResponse:
  return execute_request(
      credentials, method='post', path='/detection-jobs/build-model', body=job_configuration
  )


def get_anomaly_detection_logs(credentials: Credentials, id: str) -> List[Logs]:
  return execute_request(credentials=credentials, method='get', path=f'/detection-jobs/{id}/log')


def execute_anomaly_detection_job(credentials: Credentials, id: str) -> ExecuteResponse:
  return execute_request(credentials=credentials, method='post', path=f'/detection-jobs/{id}/execute')


def get_anomaly_detection_job_status(credentials: Credentials, id: str) -> StatusResponse:
  return execute_request(credentials=credentials, method='get', path=f'/detection-jobs/{id}/status')


def get_anomaly_detection(credentials: Credentials, id: str) -> AnomalyDetectionMetaData:
  return execute_request(credentials=credentials, method='get', path=f'/detection-jobs/{id}')


def get_anomaly_detection_table_results(credentials: Credentials, id: str) -> pd.DataFrame:
  response = execute_request(
      credentials=credentials, method='get', path=f'/detection-jobs/{id}/results/table'
  )

  data_string = StringIO(response)

  return pd.read_csv(data_string)  # pyright: reportGeneralTypeIssues=false, reportUnknownMemberType=false


def get_anomaly_detection_model_results(credentials: Credentials, id: str) -> AnomalyDetectionJobModelResult:
  return execute_request(credentials=credentials, method='get', path=f'/detection-jobs/{id}/results/model')


def poll_anomaly_detection_status(credentials: Credentials, id: str, tries_left: int = 20) -> StatusResponse:
  if tries_left < 1:
    raise ValueError("Timeout error.")

  response = get_anomaly_detection_job_status(credentials, id)
  if Status(response['status']).value == Status.FAILED.value:
    return response
  if Status(response['status']).value != Status.FINISHED.value and Status(
      response['status']
  ).value != Status.FINISHED_WITH_WARNING.value:
    sleep(2)
    return poll_anomaly_detection_status(credentials, id, tries_left - 1)

  return response
