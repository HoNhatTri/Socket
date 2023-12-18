import win32com.client as win32 
import os

outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
account = outlook.CurrentUser.AddressEntry.GetExchangeUser().PrimarySmtpAddress
ff= outlook.Folders[account].Folders("Work")
des=outlook.Folders[account].Folders("Hộp thư đến")
messages = ff.Items
for msg in messages :
    msg.Move(des)
