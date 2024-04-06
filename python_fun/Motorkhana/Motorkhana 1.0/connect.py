# These details are available on the first MySQL Workbench screen
# Usually called 'Local Instance'
import mysql.connector  # or import pymysql

dbuser = "root"  # Your MySQL username - likely 'root'
dbpass = "Xeldragon123!"  # ---- PUT YOUR PASSWORD HERE ----
# Or use the actual IP address or hostname where your MySQL server is running
dbhost = "127.0.0.1"


dbport = "3306"  # Use the correct port for MySQL (usually 3306)

dbname = "motorkhana"

connection = mysql.connector.connect(
    user=dbuser, password=dbpass, host=dbhost, port=dbport, database=dbname)
