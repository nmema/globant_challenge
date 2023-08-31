"""This module contains methos for the upload endpoint."""
from aws_helpers import rds_get_conn, s3_get_content
from fastapi import APIRouter

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
    data = s3_get_content(s3_url=s3_path)

    conn = rds_get_conn()
    cur = conn.cursor()

    query = f"""
        select column_name
        from information_schema.columns
        where
            table_schema = 'csv'
            and table_name   = '{table_id}'
        order by ordinal_position
    """

    cur.execute(query)
    query_results = cur.fetchall()

    # pylint: disable=line-too-long
    query = f"insert into csv.{table_id} ({', '.join([column[0] for column in query_results])}) values ({('%s,' * len(query_results))[:-1]})"
    cur.executemany(query, data)

    return {200: 'OK'}
