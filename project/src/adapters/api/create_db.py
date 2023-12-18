"""
##TEST PURPOSE##
create_db.py

Usage:
    This module is to create test data for mysql
    Read the rec_campaigns_small.json and insert into Mysql for Testing
"""

from fastapi import APIRouter
import mysql.connector
import json

router = APIRouter()

db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'hostname-mysql',
    'raise_on_warnings': True,
}

def create_db_function():
    try:
        # json_file_path = 'src/adapters/api/rec_campaigns_small.json'
        json_file_path = 'src/adapters/api/rec_campaigns.json'

        # current_file_path = Path(__file__)
        # project_dir = current_file_path.parent.parent.parent.parent.parent
        # json_file_path = project_dir / 'resource' / 'rec_campaigns.json'

        with open(json_file_path, 'r') as file:
            recs_data = json.load(file)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS google_recs")
        except Exception as e:
            print(e)
        try:
            cursor.execute(""" DROP TABLE google_recs.recs;""")
            cursor.execute("USE google_recs")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recs (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    image_url VARCHAR(255),
                    landing_url VARCHAR(255),
                    weight INT,
                    target_country VARCHAR(20),
                    target_gender VARCHAR(1) NULL,
                    point INT
                )
            """)
            cursor.execute("""
                CREATE INDEX idx_target_country ON recs (target_country);
            """)

            # cursor.execute("""
            #     CREATE INDEX idx_target_gender ON recs (target_gender);
            # """)


            conn.commit()
        except Exception as e:
            print(e)
        try:
            cursor.execute(""" DROP TABLE google_recs.point_user;""")
        except Exception as e:
            print(e)

        try:
            # cursor.execute("CREATE DATABASE IF NOT EXISTS google_recs")
            cursor.execute("USE google_recs")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS point_user (
                    id INT PRIMARY KEY,
                    balance VARCHAR(255),
                    timestamp DATETIME
                )
            """)

            conn.commit()
        except Exception as e:
            print(e)

        try:
            cursor.execute(""" DROP TABLE google_recs.point_history;""")
        except Exception as e:
            print(e)

        try:
            # cursor.execute("CREATE DATABASE IF NOT EXISTS google_recs")
            cursor.execute("USE google_recs")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS point_history (
                user_id INT,
                rec_id INT,
                transaction VARCHAR(20),
                point INT,
                remaining_balance INT,
                timestamp DATETIME,
                initialized VARCHAR(255),
                PRIMARY KEY (user_id, timestamp, initialized)
            )
            """)

            conn.commit()
        except Exception as e:
            print(e)

        insert_stmt = (
            "INSERT INTO google_recs.recs (id, name, image_url, landing_url, weight, target_country, target_gender, point)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            "ON DUPLICATE KEY UPDATE id=id"
        )

        for rec in recs_data:
            cursor.execute(insert_stmt, (
                rec['id'],
                rec['name'],
                rec['image_url'],
                rec['landing_url'],
                rec['weight'],
                rec['target_country'],
                rec.get('target_gender', None),
                rec['point'],
            ))

        conn.commit()
    except Exception as e:
        print(e)
        return e

    return None

@router.get("/")
def create_db():
    create_db_function()