import sqlite3
myschool=sqlite3.connect("schooltest.db")
curschool=myschool.cursor()
curschool.execute("""CREATE TABLE students (
studentid INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT (20) NOT NULL,
marks REAL);""")
myschool.close()




mysid= int(input("Enter ID: "))
myname=input("Enter name: ")
myhouse=int(input("Enter house: "))
mymarks=float(input("Enter marks: "))
        
#try block to catch exceptions
try:
    curschool=MySchool.cursor()
    curschool.execute("INSERT INTO student (StudentID, name, house, marks) VALUES (?,?,?,?)", (mysid, myname, myhouse, mymarks))
    MySchool.commit()
    print ("One record added successfully.")
    
#except block to handle exceptions    
except:
    print ("Error in operation.")
    MySchool.rollback()
        
MySchool.close()
    




