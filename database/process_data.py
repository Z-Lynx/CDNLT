import mysql.connector


def check_job_id_exist(job_id):
    try:
        # connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="jobuser",
            password="jobpassword",
            database="job_data"
        )

        # create a cursor object
        cursor = conn.cursor()

        # execute the select statement
        cursor.execute("SELECT JOB_ID FROM job_data WHERE JOB_ID = %s", (job_id,))

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
        # Connect to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="jobuser",
            password="jobpassword",
            database="job_data"
        )

        cursor = conn.cursor()

        # Prepare the SQL statement
        if check_job_id_exist(data['JOB_ID']):
            return True

        sql = "INSERT INTO job_data (JOB_ID, JOB_TITLE, JOB_ACTIVEDATE, DATE_VIEW, EMP_NAME, BENEFIT_NAME, LINK_JOB, JOB_SALARY_STRING, LOCATION_NAME_ARR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
    insert_data({
            "JOB_ID": "35BBC057",
            "JOB_TITLE": "ACCOUNTANT SPECIALIST",
            "JOB_ACTIVEDATE": "02-04-2023",
            "DATE_VIEW": "02-04-2023",
            "EMP_NAME": "CÔNG TY TNHH RV GROUP VIỆT NAM",
            "BENEFIT_ICON": [
                "fa-laptop",
                "fa-medkit",
                "fa-plane",
                "fa-taxi",
                "fa-fighter-jet",
                "fa-black-tie",
                "fa-usd",
                "fa-user-md",
                "fa-graduation-cap",
                "fa-line-chart",
                "fa-credit-card",
                "fa-money",
                "fa-briefcase",
                "fa-heartbeat"
            ],
            "BENEFIT_NAME": [
                "Laptop",
                "Chế độ bảo hiểm",
                "Du Lịch",
                "Xe đưa đón",
                "Du lịch nước ngoài",
                "Đồng phục",
                "Chế độ thưởng",
                "Chăm sóc sức khỏe",
                "Đào tạo",
                "Tăng lương",
                "Công tác phí",
                "Phụ cấp thâm niên",
                "Nghỉ phép năm",
                "CLB thể thao"
            ],
            "LINK_JOB": "https://careerbuilder.vn/vi/tim-viec-lam/accountant-specialist.35BBC057.html",
            "URL_EMP_DEFAULT": "https://careerbuilder.vn/vi/nha-tuyen-dung/cong-ty-tnhh-rv-group-viet-nam.35A90F85.html",
            "URL_LOGO_EMP": "https://images.careerbuilder.vn/employer_folders/lot5/272005/155x155/152820logo.png",
            "JOB_SALARY_STRING": "Cạnh Tranh",
            "JOB_NEW": 1,
            "JOB_TITLE_RED": "",
            "JOB_CLASS_CSS_ITEM": "",
            "JOB_PREMIUM_ICON_ITEM": 0,
            "LOCATION_NAME_ARR": [
                "Hồ Chí Minh"
            ]
        })