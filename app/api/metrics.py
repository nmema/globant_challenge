"""This module contains methos for the metrics endpoint."""
from db import get_employees_hired_above_mean_2021, get_employees_hired_by_quarter_2021
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

metrics_router = APIRouter(
    tags=['metrics'], prefix='/metrics', responses={200: {'description': 'OK'}}
)


@metrics_router.get('/hired_by_quarter', response_class=PlainTextResponse)
def get_total_employees_by_quarter() -> str:
    """Get the employees hired for each job and department in 2021 by quarter.

    Parameters
    ----------
    No parameters needed

    Returns
    -------
    str
        Result of the request. It's comma separated
    """
    data = get_employees_hired_by_quarter_2021()

    return data


@metrics_router.get('/hired_above_mean', response_class=PlainTextResponse)
def get_employees_hired_above_mean() -> str:
    """Get employees hired of each department above the mean of hired by department.

    Parameters
    ----------
    No parameters needed

    Returns
    -------
    str
        Result of the request. It's comma separated
    """
    data = get_employees_hired_above_mean_2021()

    return data
