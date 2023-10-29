# MotorKhan Web Application Report

This report provides an overview of the MotorKhan web application project, including its structure, design decisions, assumptions, and answers to specific database-related questions.

## Web Application Structure

The MotorKhan web application is built using Flask, a Python web framework, and is structured as follows:

### Routes & Functions

1. **Home Page (Route: "/")**: This is the landing page of the application, which displays a base HTML template.

2. **List Drivers (Route: "/listdrivers")**: This route displays a list of drivers from the database. It connects to the `listdrivers` function, which retrieves driver data from the database and renders the "driverlist.html" template.

3. **Driver Run Details (Route: "/driversrun_details")**: This route displays detailed information about drivers and their run performance. It connects to the `driversrun_details` function, which retrieves data from multiple tables (drivers, cars, and runs) in the database, processes it, and renders the "driversrun_details.html" template.

4. **List Courses (Route: "/listcourses")**: This route displays a list of courses from the database. It connects to the `listcourses` function, which retrieves course data from the database and renders the "courselist.html" template.

5. **Overall Result (Route: "/overall_result")**: This route shows an overall result summary for each driver, considering different courses. It connects to the `overall_result` function, which fetches and processes driver data, course data, and run results, and renders the "overall_result.html" template. The winning driver with the minimal time is highlighted with a trophy symbol (🏆).

6. **List Drivers Data (Route: "/listdriversData")**: This route displays additional driver information, including their car details. It connects to the `listdriversData` function, which retrieves and processes data from the driver and car tables and renders the "listdriversData.html" template.

7. **Show Graph (Route: "/showgraph")**: This route displays a chart of the top 5 drivers based on their overall results. It connects to the `showgraph` function, which retrieves and processes data and renders the "showgraph.html" template.

8. **Admin (Route: "/admin")**: This route is designed for administrative purposes and displays a list of junior drivers. It connects to the `admin` function, which retrieves junior driver data from the database and renders the "admin.html" template.

9. **Edit Driver (Route: "/edit_driver/<int:driver_id>")**: This route allows the editing of driver information. It connects to the `edit_driver` function, which handles both GET and POST requests for editing driver details.

10. **Delete Driver (Route: "/delete_driver/<int:driver_id>")**: This route allows the deletion of a driver. It connects to the `delete_driver` function, which handles POST requests to delete a driver.

### Templates

- **base.html**: The base HTML template used as the common structure for all pages.
- **driverlist.html**: Displays the list of drivers.
- **driversrun_details.html**: Shows detailed information about drivers and their run performance.
- **courselist.html**: Displays the list of courses.
- **overall_result.html**: Displays the overall results with a trophy symbol for the winning driver.
- **listdriversData.html**: Shows additional driver information, including car details.
- **showgraph.html**: Renders a chart of the top 5 drivers based on overall results.
- **admin.html**: Used for administrative purposes to display junior drivers.
- **edit_driver.html**: Allows editing of driver information.

## Assumptions and Design Decisions

### Assumptions

- Age is calculated based on the driver's date of birth.
- Drivers under 18 are considered junior, while those 18 or older are considered senior.
- The database structure and content follow the provided SQL file, "motorkhana_local.sql."
- There is no authentication or login system for drivers or administrators.

### Design Decisions

- The Flask framework is chosen for its simplicity and ease of use in building a web application.
- Routes are designed to logically separate different functionalities, such as listing drivers, displaying overall results, and providing administrative capabilities.
- Templates are used to maintain consistency in the application's appearance.
- For displaying the winning driver in the "Overall Result" page, a trophy (🏆) symbol is used to highlight the winner.

## Database Questions

1. **SQL Statement for Creating the Car Table**:
   ```sql
   CREATE TABLE car (
       car_num INT,
       model VARCHAR(255),
       drive_class VARCHAR(255)
   );
   ```

2. **SQL Code for Setting up the Relationship Between Car and Driver Tables**:
   The relationship between the car and driver tables is established by the "driver" table's "car" field, which references the "car_num" in the "car" table.

3. **SQL Code for Inserting Mini and GR Yaris Details Into the Car Table**:
   ```sql
   INSERT INTO car VALUES
   (11,'Mini','FWD'),
   (17,'GR Yaris','4WD');
   ```

4. **Changing the Driver_Class Default Value to 'RWD**':
   To set the default value of "RWD" for the "driver_class" field, you would need to modify the table structure using an ALTER TABLE statement:
   ```sql
   ALTER TABLE driver MODIFY COLUMN driver_class VARCHAR(255) DEFAULT 'RWD';
   ```

5. **Importance of Separate Routes for Drivers and Club Admin**:
   It is important to have separate routes for drivers and club administrators to ensure proper access control and maintain data integrity. Two specific problems that could occur if all web app facilities were available to everyone:
   - Unauthorized users could edit or delete driver information, leading to data corruption.
   - Admin-specific functionalities, like managing junior drivers, could be misused by regular drivers.

## Image Sources

The application does not use any external images apart from the 6 course diagrams provided with the project. These images are included in the application as static resources and are not externally sourced.

---

This report provides an overview of the MotorKhan web application's structure, design decisions, and answers to database-related questions. It outlines the application's functionality, routes, templates, assumptions, and design choices to create a clear understanding of the project.