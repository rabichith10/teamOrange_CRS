# connecting to neo4j, performing queries and sending automated email.

get_ipython().system('pip install neo4j')

from neo4j import GraphDatabase 
import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def fetch_customer_details():
    #connection with neo4j
    crs=GraphDatabase.driver(uri="bolt://localhost:11005")
    
    #creating a session for command execution 
    s=crs.session()
    
    #Query 1: to fetch the customer causing issue.
    q1="MATCH(c:Cars)-[:ALOTTED_TO]->(b:Bookings )<-[:REQUESTS]-(cust:Customers) where c.Color='Red' and b.Pick_Up_Location='Berlin'and b.Booking_Start_Date<= date('2019-02-15') and b.Booking_End_Date >= date('2019-02-15') RETURN cust.Customer_Id,cust.Full_Name,cust.Address,cust.Country,cust.Age,cust.Gender,cust.Email,cust.Phone"
    nodes=s.run(q1)
        
    #Query 2: load the customer causing issue to the complaints DB
    
    q1="MATCH(c:Cars)-[:ALOTTED_TO]->(b:Bookings )<-[:REQUESTS]-(cust:Customers) where c.Color='Red' and b.Pick_Up_Location='Dresden'and b.Booking_Start_Date<= date('2019-11-18') and b.Booking_End_Date >= date('2019-11-18') MERGE(comp:Complaints)-[:AGAINST]->(cust) SET comp.Customer_ID = cust.Customer_Id,comp.Full_Name = cust.Full_Name, comp.Address=cust.Address,comp.Country=cust.Country,comp.Age=cust.Age,comp.Gender=cust.Gender,comp.Email=cust.Email,comp.Phone=cust.Phone"
    nodes=s.run(q1)
    
    #Query 3: Fetch the customer list from the complaints DB
    q2="MATCH(comp:Complaints)-[:AGAINST]->(cust:Customers) RETURN comp"
    nodes2=s.run(q2)
    
    for j in nodes2:
        print("the customers list to send legal notice are:\n\n{}".format(j))
        
    # convert the neo4j object to dataframe and export the file.
    data=data=nodes2.data()
    df=pd.DataFrame(data)
    df
    df.to_csv(r'C:\Users\Acer\Desktop\df.txt', index=None, sep=' ', mode='a')
    
fetch_customer_details()

def send_email():
    # the employee email ID - sender , LegalTeam email ID - receiver.
    sender_email = '<employee@carrental.com>'
    email_password = '<123456>'
    receiver_email = '<legalteam@carrental.com>'
    
    subject = 'Customer list - to send legal notice'
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Body of the email
    
    body = 'Please find the customer details to send legal notice'
    msg.attach(MIMEText(body,'plain'))
    
    # attaching the customer list
    filename='C:/Users/Acer/Desktop/df.txt'
    attachment  = open(filename,'rb')
    
    part = MIMEBase('application','octet-stream')
    part.add_header('Content-Disposition',"attachment; filename= "+filename)
    
    
    msg.attach(part)
    text = msg.as_string()

    #the hostname and port number of carrental service should be updated below 
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()

    # senders email autentication
    server.login(sender_email,email_password)
    
    #send mail block.
    server.sendmail(sender_email,receiver_email,text )
    server.quit()

# callling the send email function

send_email()
del df

