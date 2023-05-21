import win32com.client as win32
from openpyxl import Workbook
from openpyxl import load_workbook

import os

# Path to the Excel file
excel_file_path = 'E:\\Repos\\vroom-vroom\\python_fun\\simple python works\\file.xlsx'

# Number of attachments per email
num_attachments = 1

# Outlook automation
outlook = win32.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')

# Create a new workbook
workbook = Workbook()
sheet = workbook.active

# Set column names
sheet['A1'] = 'Subject'
sheet['B1'] = 'To Email Address'
sheet['C1'] = 'Body'
sheet['D1'] = 'Attachment1'
sheet['E1'] = 'Email Sent'  # New column for email sent indication

# Save the workbook to the specified path
workbook.save(excel_file_path)
print("Excel file created successfully.")

# Instructions for the user
print("Please paste the email data into the Excel file.")
print("Ensure that the data starts from row 2, with the subject in column A, email address in column B, body in column C, and attachments in column D.")

# Wait for user confirmation to proceed
input("Press Enter to send the emails...")

# Load the Excel file
workbook = load_workbook(excel_file_path)
sheet = workbook.active

# Iterate over the rows in the Excel sheet
for row in sheet.iter_rows(min_row=2, values_only=True):
    email = row[1]  # To email address
    subject = row[0]  # Subject
    body = row[2]  # Body of the email
    email_sent = row[4]  # Email sent indication

    # Check if the email has already been sent
    if email_sent:
        print(f"Skipping email: {subject} | {email} - Email already sent.")
        continue

    # Dictionary mapping attachment numbers to file names
    attachments = {}
    for j in range(num_attachments):
        attachment_file = row[j+3]
        if attachment_file:
            attachments[j+1] = attachment_file

    mail_item = outlook.CreateItem(0)  # 0 represents mail item

    # Set email properties
    mail_item.Subject = subject
    mail_item.To = email
    mail_item.Body = body

    # Attach the PDF files
    for attachment_num, attachment_file in attachments.items():
        attachment_path = os.path.join('F:\work related', attachment_file)
        mail_item.Attachments.Add(Source=attachment_path)

    # Send the email
    try:
        mail_item.Send()
        print(f"Email sent successfully: {subject} | {email}")
        # Mark email as sent in the Excel file
        sheet.cell(row=row[0].row, column=5).value = "Sent"
    except Exception as e:
        print(f"Failed to send email: {subject} | {email} - {str(e)}")

# Save the updated workbook with email sent indications
workbook.save(excel_file_path)
print("Emails sent successfully.")

