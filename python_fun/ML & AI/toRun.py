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
employee['project'] = employee['project'].str.replace('1741','1742')
print(employee)
