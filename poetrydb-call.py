import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen
import json
import random

haslo = []
with open("haslo.txt") as file:
    for l in file:
        haslo.append(l.strip())

haslo = haslo[0]

recipients = "byronkking@gmail.com,bkking@gwu.edu"

def sendEmail(subject,body):
    msg = MIMEMultipart()
    msg['From']="aspidistraflyer@yahoo.com"
    msg['To']=recipients
    msg['Subject']=subject
    body = MIMEText(body)
    msg.attach(body)

    s = smtplib.SMTP(host="smtp.mail.yahoo.com", port=587)
    s.starttls()
    s.login("aspidistraflyer@yahoo.com", haslo)
    s.sendmail("aspidistraflyer@yahoo.com",recipients.split(","),msg.as_string())
    s.quit()
    print("Email sent successfully.")

##retrieve authors

response = urlopen('http://poetrydb.org/author')

call = response.read().decode("utf-8") 

authors = json.loads(call)

authorLists = authors['authors']

authorChoice = random.choice(authorLists)

##retrieve poems

response = urlopen('http://poetrydb.org/author/'+authorChoice.replace(" ","%20"))

call = response.read().decode("utf-8") 

poems = json.loads(call)

poemsList = []
for poem in poems:
	title = poem['title']
	poemsList.append(title)

##select poem and send email

poemsChoice = random.choice(poemsList)

author = poems[poemsList.index(poemsChoice)]['author']

lines = poems[poemsList.index(poemsChoice)]['lines']

lines = "\n".join(str(x) for x in lines)

sendEmail(poemsChoice+" by "+author,lines)
