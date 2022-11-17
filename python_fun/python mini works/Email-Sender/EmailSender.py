# for i in range(1000)
import win32com.client as win32
olApp = win32.Dispatch('Outlook.Application')
olNS = olApp.GetNameSpace('MAPI')
mail_item = olApp.CreateItem(0)
mail_item.Subject = "Just testing"
mail_item.BodyFormat = 1
mail_item.Body = "hello heyyy testing"
mail_item.Sender = "jeffrynspr@gmail.com"
mail_item.To = "1ofwork438@gmail.com"
mail_item.Display()
mail_item.Save()
