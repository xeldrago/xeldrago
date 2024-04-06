import openpyxl
from datetime import datetime, timedelta
import pywhatkit as kit

def set_reminder(description, reminder_date, phone_number):
    # Load the Excel workbook
    workbook = openpyxl.load_workbook('reminders.xlsx')
    sheet = workbook.active

    # Add a new row with the reminder details
    sheet.append([description, reminder_date, phone_number])

    # Save the updated workbook
    workbook.save('reminders.xlsx')

def send_whatsapp_message(message, phone_number, delay_minutes=1):
    # Get the current date and time
    today = datetime.now()

    # Send the WhatsApp message
    kit.sendwhatmsg(phone_number, message, today.hour, today.minute + delay_minutes)

# Example: Set a reminder and send a message
set_reminder("Dunzo - yes i made it in python ...sad", datetime(2024, 1, 14, 15, 30), "+17744447177")

# Load the Excel workbook
workbook = openpyxl.load_workbook('reminders.xlsx')
sheet = workbook.active

# Get the current date and time
today = datetime.now()

# Loop through the rows in the Excel sheet
for row in sheet.iter_rows(min_row=2, values_only=True):
    description, reminder_date, phone_number = row
    reminder_date = datetime.combine(reminder_date, datetime.min.time())  # Combine with a time for comparison

    if today.date() == reminder_date.date():
        # If today is the reminder date, send a message to the specified WhatsApp number
        message = f"Reminder: {description}"
        send_whatsapp_message(message, phone_number)
        print(f"Sent reminder for '{description}' to {phone_number}!")

