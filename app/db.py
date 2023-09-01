"""This module contains method to interact with the Database."""
import pandas as pd
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


def get_employees_hired_by_quarter_2021() -> str:
    """Query the DataBase to get total employees hired by quarter.

    Parameters
    ----------
    No parameters needed.

    Returns
    -------
    str
        Result of the query
    """
    conn = rds_get_conn()

    query = """
        with employees_by_quarter as (
            select
                dep.department,
                job.job,
                extract('quarter' from datetime::timestamp) as quarter,
                count(*) as hired
            from csv.hired_employees as emp
            left join csv.departments as dep
                on dep.id = emp.department_id
            left join csv.jobs as job
                on job.id = emp.job_id
            where extract('Year' from emp.datetime::timestamp) = 2021
            group by dep.department, job.job, quarter
            order by dep.department, job.job
        )

        select
            department,
            job,
            max(case when q.quarter = 1 then hired else 0 end) as Q1,
            max(case when q.quarter = 2 then hired else 0 end) as Q2,
            max(case when q.quarter = 3 then hired else 0 end) as Q3,
            max(case when q.quarter = 4 then hired else 0 end) as Q4
        from employees_by_quarter as q
        group by department, job
        order by department, job
    """

    dataframe = pd.read_sql(query, con=conn)

    return dataframe.to_csv(index=False)


def get_employees_hired_above_mean_2021() -> str:
    """Query the DataBase to get total employees by deparment above the mean.

    Parameters
    ----------
    No parameters needed.

    Returns
    -------
    str
        Result of the query
    """
    conn = rds_get_conn()

    query = """
        select
            dep.id,
            dep.department,
            count(emp.id) as hired
        from csv.departments dep
        join csv.hired_employees emp
            on dep.id = emp.department_id
        where extract('Year' from datetime::timestamp) = 2021
        group by dep.id, dep.department
        having count(emp.id) > (
            select
                avg(num_employees)
            from (
                select
                    dep.id,
                    count(emp.id) as num_employees
                from csv.departments dep
                join csv.hired_employees emp
                    on dep.id = emp.department_id
                where extract('Year' from datetime::timestamp) = 2021
                group by dep.id
            ) as num
        )
        order by hired desc
    """

    dataframe = pd.read_sql(query, con=conn)

    return dataframe.to_csv(index=False)
