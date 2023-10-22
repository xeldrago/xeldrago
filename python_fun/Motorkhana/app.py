import mysql.connector  # or import pymysql
from flask import Flask
from flask import render_template
from flask import Flask, render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask import Flask, render_template
import connect
import mysql.connector

app = Flask(__name__, static_url_path='/static')

dbconn = None
connection = None


def getCursor():

    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass, host=connect.dbhost,
                                         database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/listdrivers")
def listdrivers():
    try:
        connection = getCursor()
        connection.execute(
            "SELECT driver_id, first_name, surname, date_of_birth, age FROM driver;")
        driverList = connection.fetchall()
        print(driverList)  # Add this line for debugging
        return render_template("driverlist.html", driver_list=driverList)
    except Exception as e:
        # Handle the exception
        print(str(e))
        return "An error occurred while fetching the driver list."


@app.route("/driversrun_details")
def driversrun_details():
    connection = getCursor()
    connection.execute("""
        SELECT CONCAT(d.first_name, ' ', d.surname) AS Name, d.driver_id, c.model, c.drive_class, r.crs_id AS Course_ID, 
            r.seconds, r.cones, r.wd,
            (COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10) AS Total_Run
        FROM driver AS d
        LEFT JOIN car AS c ON d.car = c.car_num
        LEFT JOIN run AS r ON d.driver_id = r.dr_id
        ORDER BY d.driver_id, r.crs_id, r.run_num;
    """)
    driversrun_details = connection.fetchall()
    print(driversrun_details)
    return render_template("driversrun_details.html", driversrun_details=driversrun_details)


@app.route("/listcourses")
def listcourses():
    try:
        connection = getCursor()
        connection.execute("SELECT * FROM course;")
        courseList = connection.fetchall()
        print(courseList)  # Add this line for debugging
        return render_template("courselist.html", course_list=courseList)
    except Exception as e:
        # Handle the exception
        print(str(e))
        return "An error occurred while fetching the course list."

# Update the SQL query in your Flask app


@app.route("/overall_result")
def overall_result():
    connection = getCursor()
    connection.execute("""
        SELECT
            d.driver_id AS DriverID,
            CONCAT(d.first_name, ' ', d.surname) AS Name,
            CASE
                WHEN d.age < 18 THEN CONCAT('Junior (', d.age, ')')
                ELSE CONCAT('Senior (', d.age, ')')
            END AS NameWithAge,
            c.model AS CarModel,
            SUM(
                CASE r.crs_id
                    WHEN 'A' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseA,
            SUM(
                CASE r.crs_id
                    WHEN 'B' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseB,
            SUM(
                CASE r.crs_id
                    WHEN 'C' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseC,
            SUM(
                CASE r.crs_id
                    WHEN 'D' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseD,
            SUM(
                CASE r.crs_id
                    WHEN 'E' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseE,
            SUM(
                CASE r.crs_id
                    WHEN 'F' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS CourseF,
            SUM(
                CASE r.crs_id
                    WHEN 'A' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    WHEN 'B' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    WHEN 'C' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    WHEN 'D' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    WHEN 'E' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    WHEN 'F' THEN r.seconds + r.cones * 5 + IF(r.wd, 10, 0)
                    ELSE 0
                END
            ) AS OverallResult
        FROM driver AS d
        JOIN car AS c ON d.car = c.car_num
        JOIN run AS r ON d.driver_id = r.dr_id
        GROUP BY d.driver_id
    """)
    overall_results = connection.fetchall()
    return render_template("overall_result.html", overall_results=overall_results)


@app.route("/listdriversData")
def listdriversData():
    try:
        connection = getCursor()
        connection.execute("""
            SELECT CONCAT(first_name, ' ', surname) AS name, 
                   date_of_birth, 
                   age, 
                   caregiver, 
                   model AS car_model, 
                   drive_class
            FROM driver
            JOIN car ON driver.car = car.car_num;
        """)
        driver_list = connection.fetchall()
        print(driversrun_details)
        return render_template("listdriversData.html", driver_list=driver_list)

    except Exception as e:
        # Handle the exception
        print(str(e))
        return "An error occurred while fetching the driver list."


@app.route("/showgraph")
def showgraph():
    connection = getCursor()

    # Get the top 5 drivers based on their overall results
    connection.execute(
        "SELECT driver_id, CONCAT(first_name, ' ', surname) AS driver_name, overall_result FROM driver ORDER BY overall_result ASC LIMIT 5;"
    )
    topDrivers = connection.fetchall()

    # Create lists for driver names and results for the chart
    driverNames = [driver[1] for driver in topDrivers]
    driverResults = [driver[2] for driver in topDrivers]

    # Pass data to the template for rendering the chart
    return render_template("showgraph.html", driverNames=driverNames, driverResults=driverResults)


if __name__ == "__main__":
    app.run(debug=True)
