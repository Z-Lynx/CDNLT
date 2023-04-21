import os
import mysql.connector
from dotenv import load_dotenv
from helpper.utils import *

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TABLE = os.getenv('TABLE')

if os.environ.get('DOCKER_CONTAINER') == "true":
    LOCALHOST = os.getenv('LOCALHOSTDOCKER')
else:
    LOCALHOST = os.getenv('LOCALHOST')

JOBS = JOB_ID + ", " + JOB_TITLE + ", " + JOB_ACTIVEDATE + ", " + DATE_VIEW + ", " + EMP_NAME + ", " + BENEFIT_NAME + ", " + LINK_JOB + ", " + JOB_SALARY_STRING + ", " + LOCATION_NAME_ARR

def check_job_id_exist(job_id):
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

        # execute the select statement
        cursor.execute("SELECT " + JOB_ID + " FROM " + TABLE + " WHERE " + JOB_ID + " = %s", (job_id,))

        # fetch the record
        record = cursor.fetchone()

        # check if the record exists
        if record is not None:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        print("Failed to check if JOB_ID exists in MySQL table: {}".format(error))


def insert_data(data):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        cursor = conn.cursor()

        # Prepare the SQL statement
        if check_job_id_exist(data[JOB_ID]):
            return False

        sql = "INSERT INTO " + TABLE + " (" + JOBS + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data[JOB_ID], data[JOB_TITLE], data[JOB_ACTIVEDATE], data[DATE_VIEW], data[EMP_NAME],
               ','.join(data[BENEFIT_NAME]), data[LINK_JOB], data[JOB_SALARY_STRING],
               ','.join(data[LOCATION_NAME_ARR]))
        cursor.execute(sql, val)
        # Commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False


def edit_job_by_id(job_id, data):
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
        if not check_job_id_exist(job_id):
            return False
        # prepare the SQL query
        sql_query = "UPDATE " + TABLE + " SET " + JOB_TITLE + "=%s, " + JOB_ACTIVEDATE + "=%s, " \
                    + DATE_VIEW + "=%s, " + EMP_NAME + "=%s, " + BENEFIT_NAME + "=%s, " + LINK_JOB + "=%s, " \
                    + JOB_SALARY_STRING + "=%s, " + LOCATION_NAME_ARR + "=%s WHERE " + JOB_ID + "=%s"

        # extract the values from the data dictionary
        values = (
            data[JOB_TITLE], data[JOB_ACTIVEDATE], data[DATE_VIEW], data[EMP_NAME],
            ','.join(data[BENEFIT_NAME]), data[LINK_JOB], data[JOB_SALARY_STRING],
            ','.join(data[LOCATION_NAME_ARR]),
            job_id
        )
        # execute the SQL query with the values
        cursor.execute(sql_query, values)

        # commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False


def remove_job_by_id(job_id):
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
        if not check_job_id_exist(job_id):
            return False
        # prepare the SQL query
        sql_query = "DELETE FROM " + TABLE + " WHERE " + JOB_ID + " = %s"

        # execute the SQL query with the job_id parameter
        cursor.execute(sql_query, (job_id,))

        # commit the changes to the database
        conn.commit()

        cursor.close()
        conn.close()
        return True
    
    
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False


def check_user(username, password):
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host=LOCALHOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Prepare the SQL query to check for user and password
        sql_query = "SELECT * FROM Member WHERE user = %s AND pwd = %s"

        # Execute the SQL query with the username and password parameters
        cursor.execute(sql_query, (username, password))

        # Fetch the first row from the result set
        row = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # If the row exists, return True
        if row:
            return True

        # If the row doesn't exist, return False
        return False

    except mysql.connector.Error as error:
        print("Failed to query MySQL database: {}".format(error))
        return False


if __name__ == '__main__':
    # debug
    pass
