import os
import sys

# add the directory containing the scraper module to the Python path
scraper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(scraper_path)

from fastapi import FastAPI
from database.process_data import *
from scraper.jobs_scraper import get_data
from utils import *
# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TABLE = os.getenv('TABLE')
LOCALHOST = os.getenv('LOCALHOST')

app = FastAPI()


@app.get('/search_jobs_title/')
def search_job(title):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()
        query = "SELECT * FROM " + TABLE + " WHERE " + JOB_TITLE + " LIKE '%" + title + "%'"
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}

    return dict_rows


@app.get('/search_jobs_country/')
def search_country(country):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()

        query = "SELECT * FROM " + TABLE + " WHERE " + LOCATION_NAME_ARR + " LIKE '%" + country + "%'"
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}
    return dict_rows


@app.get('/top_salary/')
def search_country(top):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()

        query = "SELECT * FROM " + TABLE + " WHERE " + JOB_SALARY_STRING + " IS NOT NULL ORDER BY CAST(REPLACE(SUBSTRING_INDEX(" + JOB_SALARY_STRING + ", ' - ', -1), ' Tr VND', '') AS DECIMAL(10,2)) DESC LIMIT " + top
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}

    return dict_rows


@app.get('/new_job/')
def newjob():
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()

        query = "SELECT * FROM " + TABLE + " WHERE " + JOB_ACTIVEDATE + " = (SELECT MAX(" + JOB_ACTIVEDATE + ") FROM " + TABLE + ")"

        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}
    return dict_rows


@app.get('/jobs/page')
def jobs_page(limit):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()

        query = "SELECT * FROM " + TABLE + " LIMIT " + limit
        cursor.execute(query)

        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to dictionary
        rows = cursor.fetchall()

        dict_rows = []
        for row in rows:
            dict_row = {}
            for i, column in enumerate(columns):
                dict_row[column] = row[i]
            dict_rows.append(dict_row)
    except:
        return {'status': 400, 'message': 'Lỗi'}
    return dict_rows


@app.post('/add')
def add(job_id: str, job_title: str, job_activedate: str, date_view: str, emp_name: str, benefit_name: str, link_job: str, job_salary_string: str, location_name_arr: str):
    data = {
        JOB_ID: job_id,
        JOB_TITLE: job_title,
        JOB_ACTIVEDATE: job_activedate,
        DATE_VIEW: date_view,
        EMP_NAME: emp_name,
        BENEFIT_NAME: benefit_name,
        LINK_JOB: link_job,
        JOB_SALARY_STRING: job_salary_string,
        LOCATION_NAME_ARR: location_name_arr
    }
    val = insert_data(data)
    if val:
        return {'status': 200, 'message': 'Thêm Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}


@app.put('/jobs/{job_id}')
def edit_job(job_id: str, job_title: str, job_activedate: str, date_view: str, emp_name: str, benefit_name: str, link_job: str, job_salary_string: str, location_name_arr: str):
    data = {
        JOB_ID: job_id,
        JOB_TITLE: job_title,
        JOB_ACTIVEDATE: job_activedate,
        DATE_VIEW: date_view,
        EMP_NAME: emp_name,
        BENEFIT_NAME: benefit_name,
        LINK_JOB: link_job,
        JOB_SALARY_STRING: job_salary_string,
        LOCATION_NAME_ARR: location_name_arr
    }

    if edit_job_by_id(job_id, data):
        return {'status': 200, 'message': 'Sửa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}

@app.delete('/jobs/{job_id}')
def remove_job(job_id: str):
    val = remove_job_by_id(job_id)
    print(val)
    if val:
        return {'status': 200, 'message': 'Xóa Thành Công'}
    return {'status': 400, 'message': 'Lỗi'}


@app.get('/scraper')
def scraper():
    get_data()
    return {"status": "Update done"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=8000, reload=True)
