"""Models used by the API."""
from typing import List

from pydantic import BaseModel


class JobsModel(BaseModel):
    """Model for the jobs table."""

    id: int
    job: str


class JobsList(BaseModel):
    """Model used by the batch/jobs endpoint."""

    data: List[JobsModel]


class DeparmentsModel(BaseModel):
    """Model for the deparments table."""

    id: int
    department: str


class DeparmentsList(BaseModel):
    """Model used by the batch/deparments endpoint."""

    data: List[DeparmentsModel]


class HiredEmployeesModel(BaseModel):
    """Model for the hired_employees table."""

    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int


class HiredEmployeesList(BaseModel):
    """Model used by the batch/hired_employees endpoint."""

    data: List[HiredEmployeesModel]
