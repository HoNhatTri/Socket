import win32com.client as win32 
import os

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
account = outlook.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress
inbox= outlook.Folders[account].Folders("Hộp thư đến")

#Choosed_Subject = ""
#Choosed_Sender_Name = ""
#Choosed_Content = ""
#Choosed_EmailAddress = ""
#filter_querry_emailaddress = f"@SQL=\"http://schemas.microsoft.com/mapi/proptag/0x0C1F001F\" like '%{Choosed_EmailAddress}%'"
#filter_querry_sendername=f"@SQL=\"urn:schemas:httpmail:sender\" like '%{Choosed_Sender_Name}%'"
#filter_querry_subject=f"@SQL=\"urn:schemas:httpmail:subject\" like '%{Choosed_Subject}%'"
#filter_querry_content = f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{Choosed_Content}%'"

request_filter = "ahihi@testing.com"
project_folder = outlook.Folders[account].Folders("Project")
filtered_emails = inbox.Items.Restrict(f"[SenderEmailAddress] = '{request_filter}'")
for email in filtered_emails:
      email.Move(project_folder)
request_filter = "ahuu@testing.com"
project_folder = outlook.Folders[account].Folders("Project")
filtered_emails = inbox.Items.Restrict(f"[SenderEmailAddress] = '{request_filter}'")
for email in filtered_emails:
      email.Move(project_folder)


request_filter = "urgent"
important_folder = outlook.Folders[account].Folders("Important")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:subject\" like '%{request_filter}%'")
for email in filtered_emails:
      email.Move(important_folder)
request_filter = "ASAP"
important_folder = outlook.Folders[account].Folders("Important")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:subject\" like '%{request_filter}%'")
for email in filtered_emails:
      email.Move(important_folder)

request_filter = "report"
work_folder = outlook.Folders[account].Folders("Work")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
for email in filtered_emails:
    email.Move(work_folder)
request_filter = "meeting"
work_folder = outlook.Folders[account].Folders("Work")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
for email in filtered_emails:
    email.Move(work_folder)

request_filter = "virus"
spam_folder = outlook.Folders[account].Folders("Spam")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:subject\" like '%{request_filter}%'" or f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
for email in filtered_emails:
      email.Move(spam_folder)
request_filter = "hack"
spam_folder = outlook.Folders[account].Folders("Spam")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:subject\" like '%{request_filter}%'" or f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
for email in filtered_emails:
      email.Move(spam_folder)
request_filter = "crack"
spam_folder = outlook.Folders[account].Folders("Spam")
filtered_emails = inbox.Items.Restrict(f"@SQL=\"urn:schemas:httpmail:subject\" like '%{request_filter}%'" or f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{request_filter}%'")
for email in filtered_emails:
      email.Move(spam_folder)


#Choosed_Subject = "Phòng đào tạo"
#Choosed_Sender_Name = "Quý"
#Choosed_Content = "Chào em"
#Choosed_EmailAddress = "khaothi2@hcmus.edu.vn"
#filter_querry_emailaddress = f"@SQL=\"http://schemas.microsoft.com/mapi/proptag/0x0C1F001F\" like '%{Choosed_EmailAddress}%'"
#filter_querry_sendername=f"@SQL=\"urn:schemas:httpmail:sender\" like '%{Choosed_Sender_Name}%'"
#filter_querry_subject=f"@SQL=\"urn:schemas:httpmail:subject\" like '%{Choosed_Subject}%'"
#filter_querry_content = f"@SQL=\"urn:schemas:httpmail:textdescription\" like '%{Choosed_Content}%'"
#messages = inbox.Items.Restrict(filter_querry_emailaddress)
#messages.Sort("[ReceivedTime]",True)
#for msg in messages:
      #print(msg.SenderName + " " + str(msg.ReceivedTime))