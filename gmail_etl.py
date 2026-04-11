import tweepy
import pandas as pd 
import json
import datetime
import s3fs 
import imaplib
import email
from email.message import EmailMessage


imap = 'imap.gmail.com'
imap_port = 993

email_address ='evekon2023@gmail.com'
email_password ='Shubham7001' 
                
imap = imaplib.IMAP4_SSL(imap, imap_port)
imap.login(email_address, email_password)



imap.select('INBOX')
today = datetime.date.today()
    
start_date = today - datetime.timedelta(days=20)
    

end_date = today + datetime.timedelta(days=0)
print(start_date)
print(end_date)
print("email fetched")

# Search for email messages within the date range
search_string = f'(SINCE "{start_date.strftime("%d-%b-%Y")}" BEFORE "{end_date.strftime("%d-%b-%Y")}")'
status, email_ids = imap.search(None, search_string)
print(email_ids)
print('search_string')
print(search_string)

list=[]
# Loop through each message ID and retrieve its contents
for email_id in email_ids[0].split():

    # Use the fetch method to retrieve the contents of the message
    status, email_data = imap.fetch(email_id, '(RFC822)')
    raw_email = email_data[0][1]

    # Parse the raw email data into an email message object
    msg = email.message_from_bytes(raw_email)
    list.append(msg)
    print("getting messages ")
    print(f"Subject: {msg['Subject']}")
    print(f"From: {msg['From']}\n")
    df=pd.DataFrame(list)
    df.to_csv("test_gmail.csv")

    


    #logging.warning(msg)