import os
import sys

from starlette.staticfiles import StaticFiles

# add the directory containing the db module to the Python path
scraper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(scraper_path)

from db.database_utils import *
from db.jobs_scraper import get_data
from helpper.utils import *
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

if os.environ.get('DOCKER_CONTAINER') == "true":
    LOCALHOST = os.getenv('LOCALHOSTDOCKER')
    TEMPLATES = os.getenv('TEMPLATESDOCKER')
else:
    LOCALHOST = os.getenv('LOCALHOST')
    TEMPLATES = os.getenv('TEMPLATES')

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TABLE = os.getenv('TABLE')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=f"{TEMPLATES}/static"), name="static")
templates = Jinja2Templates(directory=TEMPLATES)


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/login')
async def login(user, pwd):
    try:
        if(check_user(user, pwd)):
            return {"status": 200, "messege": "success"}
        return {"status": 400, "messege": "error"}
    except Exception as e:
        return {"status": 200, "messege": e}

@app.get("/title", response_class=HTMLResponse)
async def read_title(request: Request):
    return templates.TemplateResponse("title.html")


@app.post("/title", response_class=HTMLResponse)
async def do_search(request: Request, title: str = Form(...)):
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

        # define the search query
        query = f"SELECT * FROM {TABLE} WHERE {JOB_TITLE} LIKE '%{title}%'"

        # execute the query
        cursor.execute(query)

        # get the results
        results = cursor.fetchall()

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

        # close the database connection
        cursor.close()
        conn.close()
        return templates.TemplateResponse("title.html", {'request': request, "results": dict_rows})

    except Exception as e:
        print(e)
        return templates.TemplateResponse("title.html", {'request': request, "results": []})


@app.get("/suggest")
async def suggest(title: str):
    try:
        print(title)
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # create a cursor object
        cursor = conn.cursor()

        # define the search query
        query = f"SELECT * FROM {TABLE} WHERE {JOB_TITLE} LIKE '%{title}%'"

        # execute the query
        cursor.execute(query)

        # get the results
        results = cursor.fetchall()

        # extract the titles from the results
        titles = [result[1] for result in results]

        # close the database connection
        cursor.close()
        conn.close()

        return {"suggestions": titles}
    except Exception as e:
        print(e)
        return {"suggestions": []}


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
