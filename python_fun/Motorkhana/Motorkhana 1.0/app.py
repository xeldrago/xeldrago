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
    connection.execute(
        "SELECT driver_id, CONCAT(first_name, ' ', surname) FROM driver;")
    driver_list = connection.fetchall()

    # Fetch driver run details
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

    return render_template("driversrun_details.html", driversrun_details=driversrun_details, driver_list=driver_list)


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
                WHEN d.age < 18 THEN CONCAT('(', d.age, ')')
                ELSE ''
            END AS JuniorTag,
            c.model AS CarModel,
            MIN(
                COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10
            ) AS OverallResult,
            MIN(
                CASE r.crs_id WHEN 'A' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseA,
            MIN(
                CASE r.crs_id WHEN 'B' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseB,
            MIN(
                CASE r.crs_id WHEN 'C' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseC,
            MIN(
                CASE r.crs_id WHEN 'D' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseD,
            MIN(
                CASE r.crs_id WHEN 'E' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseE,
            MIN(
                CASE r.crs_id WHEN 'F' THEN COALESCE(r.seconds, 0) + COALESCE(r.cones, 0) * 5 + COALESCE(r.wd, 0) * 10 ELSE NULL END
            ) AS CourseF
        FROM driver AS d
        LEFT JOIN car AS c ON d.car = c.car_num
        LEFT JOIN run AS r ON d.driver_id = r.dr_id
        GROUP BY d.driver_id
        ORDER BY CASE WHEN OverallResult > 0 THEN OverallResult ELSE 99999 END ASC
    """)
    overall_results = connection.fetchall()

    # Identify the top 5 drivers
    top_5_drivers = overall_results[:5]

    # Find drivers with "NQ" results
    nq_drivers = [driver for driver in overall_results if driver[4] == 0]

    return render_template("overall_result.html", top_5_drivers=top_5_drivers, nq_drivers=nq_drivers)


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
                   drive_class,
                   driver_id
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
def show_bar_graph():
    connection = getCursor()

    # Get the top 5 drivers based on their overall results
    connection.execute(
        "SELECT CONCAT(driver.first_name, ' ', driver.surname) AS driver_name, "
        "SUM(COALESCE(run.seconds, 0) + COALESCE(run.cones, 0) * 5 + COALESCE(run.wd, 0) * 10) AS overall_result "
        "FROM driver "
        "LEFT JOIN run ON driver.driver_id = run.dr_id "
        "GROUP BY driver.driver_id "
        "ORDER BY overall_result ASC LIMIT 5;"
    )
    topDrivers = connection.fetchall()

    # Create lists for driver names and results for the chart
    driverNames = [driver[0] for driver in topDrivers]
    driverResults = [driver[1] for driver in topDrivers]

    # Pass data to the template for rendering the chart
    return render_template("showgraph.html", driverNames=driverNames, driverResults=driverResults)



@app.route("/admin")
def admin():
    # Fetch the list of junior drivers
    connection = getCursor()
    connection.execute(
        "SELECT driver_id, first_name, surname, date_of_birth, age FROM driver WHERE age < 18;")
    junior_drivers = connection.fetchall()
    return render_template("admin.html", junior_drivers=junior_drivers)


@app.route("/add_driver", methods=["POST"])
def add_driver():
    connection = getCursor()
    first_name = request.form["first_name"]
    surname = request.form["surname"]
    date_of_birth = request.form["date_of_birth"]
    car = request.form.get("car")

    # Insert driver information into the database
    connection.execute("INSERT INTO driver (first_name, surname, date_of_birth, car) VALUES (%s, %s, %s, %s);",
                       (first_name, surname, date_of_birth, car))
    connection.commit()
    flash("Driver added successfully", "success")
    return redirect(url_for("admin"))


@app.route("/edit_driver/<int:driver_id>", methods=["GET", "POST"])
def edit_driver(driver_id):
    connection = getCursor()
    if request.method == "POST":
        first_name = request.form["first_name"]
        surname = request.form["surname"]
        date_of_birth = request.form["date_of_birth"]

        # Update driver information in the database
        connection.execute("UPDATE driver SET first_name = %s, surname = %s, date_of_birth = %s WHERE driver_id = %s;",
                           (first_name, surname, date_of_birth, driver_id))
        connection.commit()
        flash("Driver information updated successfully", "success")
        return redirect(url_for("admin"))
    else:
        # Fetch the driver's information to pre-fill the form
        connection.execute(
            "SELECT driver_id, first_name, surname, date_of_birth FROM driver WHERE driver_id = %s;", (driver_id,))
        driver = connection.fetchone()
        if driver:
            return render_template("edit_driver.html", driver=driver)
        else:
            flash("Driver not found", "danger")
            return redirect(url_for("admin"))


@app.route("/delete_driver/<int:driver_id>", methods=["POST"])
def delete_driver(driver_id):
    connection = getCursor()
    connection.execute(
        "DELETE FROM driver WHERE driver_id = %s;", (driver_id,))
    connection.commit()
    flash("Driver deleted successfully", "success")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
