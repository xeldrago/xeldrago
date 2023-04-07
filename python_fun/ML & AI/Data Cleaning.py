import numpy as np
import pandas as pd
employee = pd.read_csv(r'E:\Repos\vroom-vroom\python_fun\ML & AI\Table.csv')
print(employee)
employee.drop_duplicates(subset="Name", keep="first", inplace=True)
print(employee)
missing = employee.isnull()
print(missing)
del employee['Sl.No']
print(employee)
employee['Project'] = employee['Project'].replace('1826', 'frames')
print(employee)
employee.columns = ['Names', 'Phonenumber', 'domains', 'project', 'calc']
print(employee)
