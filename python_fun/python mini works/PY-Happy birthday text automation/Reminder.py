import openpyxl
from datetime import datetime
import pywhatkit as kit
import time

def send_whatsapp_message(message, phone_number, reminder_datetime):
    # Convert phone_number to string and add a country code if needed
    phone_number_str = str(phone_number)  # Replace this line based on your requirements

    # Calculate the time difference until the scheduled time
    time_difference = reminder_datetime - datetime.now()

    # Ensure the time difference is non-negative
    delay_seconds = max(0, time_difference.total_seconds())
    kit.sendwhatmsg(phone_number_str, message, reminder_datetime.hour, reminder_datetime.minute + 1)

# Load the Excel workbook
workbook = openpyxl.load_workbook('reminders.xlsx')
sheet = workbook.active

# Get the current date and time
today = datetime.now()

# Loop through the rows in the Excel sheet
for row in sheet.iter_rows(min_row=2, values_only=True):
    description, reminder_datetime, phone_number = row

    # Ensure reminder_datetime is not None before processing
    if reminder_datetime:
        # If today is the reminder date, send a message to the specified WhatsApp number
        message = f"Reminder: {description}"
        send_whatsapp_message(message, phone_number, reminder_datetime)
        print(f"Sent reminder for '{description}' to {phone_number}!")
