"""This module contains methos for the upload endpoint."""
from aws_helpers import s3_get_content
from db import insert_rows
from fastapi import APIRouter
from models import DeparmentsList, HiredEmployeesList, JobsList

upload_router = APIRouter(
    tags=['upload'], prefix='/upload', responses={200: {'description': 'OK'}}
)


@upload_router.post('/s3/{table_id}')
def upload_from_s3(table_id: str, s3_path: str) -> dict:
    """Upload S3 object to AWS RDS.

    Parameters
    ----------
    table_id : string
        Name of the table located in RDS.
    s3_path : string
        S3 URL of the object.

    Returns
    -------
    dict
        Status of the request.
    """
    records = s3_get_content(s3_url=s3_path)

    try:
        insert_rows(
            table_id=table_id,
            records=records,
        )
    except Exception as error:  # pylint: disable=W0718
        return {'Error': error}

    return {200: 'OK'}


@upload_router.post('/batch/jobs')
def batch_jobs(data: JobsList) -> dict:
    """Upload records to the jobs table on AWS RDS.

    Parameters
    ----------
    data : JobList
        Content to upload.

    Returns
    -------
    dict
        Status of the request.
    """
    rows = data.data

    records = []
    for row in rows:
        records.append((row.id, row.job))

    try:
        insert_rows(
            table_id='jobs',
            records=records,
        )
    except Exception as error:  # pylint: disable=W0718
        return {'Error': error}

    return {200: 'OK'}


@upload_router.post('/batch/departments')
def batch_departments(data: DeparmentsList) -> dict:
    """Upload records to the departments table on AWS RDS.

    Parameters
    ----------
    data : DeparmentsList
        Content to upload.

    Returns
    -------
    dict
        Status of the request.
    """
    rows = data.data

    records = []
    for row in rows:
        records.append((row.id, row.department))

    try:
        insert_rows(
            table_id='departments',
            records=records,
        )
    except Exception as error:  # pylint: disable=W0718
        return {'Error': error}

    return {200: 'OK'}


@upload_router.post('/batch/hired_employees')
def batch_hiredemployees(data: HiredEmployeesList) -> dict:
    """Upload records to the hired_employees table on AWS RDS.

    Parameters
    ----------
    data : HiredEmployeesList
        Content to upload.

    Returns
    -------
    dict
        Status of the request.
    """
    rows = data.data

    records = []
    for row in rows:
        records.append((row.id, row.name, row.datetime, row.department_id, row.job_id))

    try:
        insert_rows(
            table_id='hired_employees',
            records=records,
        )
    except Exception as error:  # pylint: disable=W0718
        return {'Error': error}

    return {200: 'OK'}
