import win32com.client as win32 
import os

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
account = outlook.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress
inbox= outlook.Folders[account].Folders("Hộp thư đến")

request_filter = "report"
work_folder = outlook.Folders[account].Folders("Work")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
filtered_emails.Sort("[ReceivedTime]",True)
for email in filtered_emails:
      print(email.SenderName + " " + str(email.ReceivedTime))
request_filter = "meeting"
work_folder = outlook.Folders[account].Folders("Work")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
filtered_emails.Sort("[ReceivedTime]",True)
for email in filtered_emails:
      print(email.SenderName + " " + str(email.ReceivedTime))