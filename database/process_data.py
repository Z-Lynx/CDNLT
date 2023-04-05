import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
TABLE = os.getenv('TABLE')
LOCALHOST = os.getenv('LOCALHOST')

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
        cursor.execute("SELECT JOB_ID FROM "+TABLE+" WHERE JOB_ID = %s", (job_id,))

        # fetch the record
        record = cursor.fetchone()

        # check if the record exists
        if record is not None:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        print("Failed to check if JOB_ID exists in MySQL table: {}".format(error))

    finally:
        # close the cursor and database connection
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


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
        if check_job_id_exist(data['JOB_ID']):
            return True

        sql = "INSERT INTO " + TABLE + " (JOB_ID, JOB_TITLE, JOB_ACTIVEDATE, DATE_VIEW, EMP_NAME, BENEFIT_NAME, LINK_JOB, JOB_SALARY_STRING, LOCATION_NAME_ARR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data['JOB_ID'], data['JOB_TITLE'], data['JOB_ACTIVEDATE'], data['DATE_VIEW'], data['EMP_NAME'],
               ','.join(data['BENEFIT_NAME']), data['LINK_JOB'], data['JOB_SALARY_STRING'], ','.join(data['LOCATION_NAME_ARR']))
        cursor.execute(sql, val)

        # Commit the changes to the database
        conn.commit()

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))
        return False

    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            return True
        return False


if __name__ == '__main__':
    # debug
    pass
