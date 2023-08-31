"""This module contains method to interact with the Database."""
from aws_helpers import rds_get_conn


def insert_rows(table_id: str, records: list) -> None:
    """Insert rows on AWS RDS.

    Parameters
    ----------
    table_id : string
        Name of the table located in RDS.
    records : list
        Records to upload.

    Returns
    -------
    None
    """
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
    cur.executemany(query, records)
    conn.commit()

    cur.close()
    conn.close()
