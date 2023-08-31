"""This module contains functions to work with AWS."""
import csv
import json

import boto3
import psycopg2


def sm_get_secret(secret_name: str) -> dict:
    """Get values from AWS Secrets Manager.

    Parameters
    ----------
    secret_name : string
        Name of the secret stored in Secrets Manager.

    Returns
    -------
    dict
        Dictionary with the values stored.
    """
    # https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html
    client = boto3.client('secretsmanager', region_name='us-west-2')
    secrets = client.get_secret_value(SecretId=secret_name)
    return json.loads(secrets['SecretString'])


def rds_get_conn() -> psycopg2.extensions.connection:
    """Get connection of Amazon RDS.

    Parameters
    ----------
    No parameters needed.

    Returns
    -------
    psycopg2.extensions.connection
        Connection to the DB.
    """
    secrets = sm_get_secret('globant_rds')

    conn = psycopg2.connect(
        host=secrets['ENDPOINT'],
        port=secrets['PORT'],
        database=secrets['DBNAME'],
        user=secrets['USER'],
        password=secrets['PASSWORD'],
        sslrootcert="SSLCERTIFICATE",
    )

    return conn


def s3_get_content(s3_url) -> list:
    """Get content of objects stored in S3.

    Objects must be CSV file type.

    Parameters
    ----------
    s3_url : string
        S3 URL of the object to download.

    Returns
    -------
    list
        List with tuples.
    """
    bucket, key = s3_url.replace('s3://', '').split('/', 1)

    client = boto3.client('s3', region_name='us-west-2')
    s3_object = client.get_object(Bucket=bucket, Key=key)

    body = s3_object['Body'].read().decode('utf-8')

    data = []
    for row in csv.reader(body.split('\r\n')):
        row_with_nulls = [None if value == '' else value for value in row]
        data.append(tuple(row_with_nulls))

    return data
