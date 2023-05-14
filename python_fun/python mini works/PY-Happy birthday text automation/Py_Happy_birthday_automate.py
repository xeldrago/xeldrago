import openpyxl
from datetime import datetime
import pywhatkit as kit

# Load the Excel workbook
workbook = openpyxl.load_workbook('birthdays.xlsx')
sheet = workbook.active

# Get the current date and time
today = datetime.now()

# Loop through the rows in the Excel sheet
for row in sheet.iter_rows(min_row=2, values_only=True):
    name, birthday, phone_number = row
    if birthday.month == today.month and birthday.day == today.day:
        # If today is the person's birthday, send a birthday message to their WhatsApp number
        message = f"Happy birthday, {name}!"
        kit.sendwhatmsg(phone_number, message, today.hour, today.minute + 1)
        print(f"Sent birthday message to {name} at {phone_number}!")
