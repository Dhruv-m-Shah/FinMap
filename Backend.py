# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 23:54:38 2019

@author: Dhruv Shah
"""

from opencage.geocoder import OpenCageGeocode
import threading
import time
import smtplib 
from plaid import Client
from fpdf import FPDF
from flask import Flask, render_template, jsonify, request 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

def foreground():

    
    @app.route('/')
    def index():
        return render_template('home.html')
    
    
    @app.route('/_get_data/', methods=['POST'])
    def _get_data():
        response = client.Transactions.get(access_token,
                                           start_date= enddate(),
                                           end_date= startdate())
        transactions = response['transactions']
        
        # Manipulate the count and offset parameters to paginate
        # transactions and retrieve all available data
        while len(transactions) < response['total_transactions']:
                response = client.Transactions.get(access_token,
                                               start_date=enddate(),
                                               end_date=startdate(),
                                               offset=len(transactions)
                                              )
                transactions.extend(response['transactions'])
        key = 'Enter Geocoder Key'
        geocoder = OpenCageGeocode(key)
        for i in range(len(transactions)):
            query = transactions[i]['location']['address']
            results = geocoder.geocode(query)
            transactions[i]['lat'] = results[0]['geometry']['lat']
            transactions[i]['lng'] = results[0]['geometry']['lng']
            
        myList = []

        return jsonify({'data': transactions})
    
    
    if __name__ == "__main__":
        app.run(debug=True)

client = Client(client_id='', secret='', public_key='', environment='sandbox')

access_token =''


def get_date():
    localtime = time.localtime(time.time())
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    date = str(localtime[2])+" "+months[localtime[1]-1]+" "+str(localtime[0])
    return date

def header_and_title():
    response = client.Identity.get(access_token)
    accounts = response['accounts']
    for account in accounts:
        identities = account['owners']
    global pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(-1)
    pdf.cell(0, 5, identities[0]['names'][0], ln=1)
    pdf.cell(-1)
    pdf.cell(0, 5, identities[0]['addresses'][0]['data']['street'], ln=1)
    pdf.cell(-1)
    pdf.cell(0, 5, identities[0]['addresses'][0]['data']['region']+" "+ identities[0]['addresses'][0]['data']['postal_code'], ln=1)
    pdf.cell(-1)
    pdf.cell(0, 5, get_date(), ln=1)
    pdf.cell(200, 10, txt="Weekly Financial Report", ln=1, align="C")

def startdate():
    localtime = time.localtime(time.time())
    startdate = ""
    startdate+= str(localtime[0])+"-"
    if(localtime[1]<10):
        startdate+="0"+str(localtime[1])+"-"
    else:
        startdate+=+ tr(localtime[1])+"-"
    if(localtime[2]<10):
        startdate+= "0" + str(localtime[2])
    else:
        startdate+=str(localtime[2])
    return startdate

def enddate():
    months_31 = [1, 3, 5, 7, 8, 10, 12]
    months_30 = [4, 6, 9, 11]
    months_28 = [2]
    localtime = time.localtime(time.time())
    subtract_month = 0
    subtract_day = 0
    subtract_year = 0
    year = 0
    month= 0
    day = 0
    if(localtime[2]<=7):
        subtract_month = 1
    if(month==1):
        subtract_year = 1
    year = localtime[0]
    month = localtime[1]
    day = localtime[2]
    if(subtract_year == 1):
        year-=1
    if(subtract_month == 1):
        if(month == 1):
            month = 12
        else:
            month-=1
    if(day<=7):
        if (month == 3):
            if((year%100 != 0 and year%4==0) or year%400 == 0):
                day = day-7+29
            else:
                day = day-7+28
        elif(month in months_31):
            day = day-7+31
        else:
            day = day-7+30
    else:
        day = day-7
    day = str(day)
    month = str(month)
    year = str(year)
    if(int(day)<10):
        
        day = "0"+day
    if(int(month)<10):
        
        month = "0"+month
    return str(year)+"-"+month+"-"+day
    
    
        

def add_weekly_transactions():
    
    response = client.Transactions.get(access_token,
                                       start_date= enddate(),
                                       end_date= startdate())
    transactions = response['transactions']
    
    # Manipulate the count and offset parameters to paginate
    # transactions and retrieve all available data
    while len(transactions) < response['total_transactions']:
        response = client.Transactions.get(access_token,
                                           start_date=enddate(),
                                           end_date=startdate(),
                                           offset=len(transactions)
                                          )
        transactions.extend(response['transactions'])
    
    for i in range(len(transactions)):
        temp = []
        temp.append(transactions[i]['date'])
        temp.append(transactions[i]['name'][0:17])
        if(transactions[i]['amount'] < 0):
            temp.append("")
            temp.append(str(transactions[i]['amount']*-1))
        else:
            temp.append(str(transactions[i]['amount']))
            temp.append("")
        data.append(temp)
            
def make_table():
    global data
    data = [["Date", "Transaction Description", "Withdrawls", "Deposits"]]
    add_weekly_transactions()
    spacing = 3
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    pdf.cell(2)
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)
        pdf.cell(2)
        pdf.output(str(time.localtime()[2])+"-"+str(time.localtime()[1])+"-"+str(time.localtime()[0])+".pdf") 
def send_email():
    msg = MIMEMultipart()
    msg['From'] = 'shatdatt5198@gmail.com'
    msg['To'] = 'backyard.green.house.data@gmail.com'
    msg['Subject'] = "test"
    body = "this is the body"
    msg.attach(MIMEText(body, 'plain'))
    filename = str(time.localtime()[2])+"-"+str(time.localtime()[1])+"-"+str(time.localtime()[0])+".pdf"
    attachment  = open(r"Enter path" + filename  , "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p)
    gmail_user = 'Enter User'
    gmail_pass = 'Enter Pass'
    to = ['Recipient']
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pass)
    text = msg.as_string()
    server.sendmail(gmail_user, to, text)
    server.close()

def make_weekly_transaction_email():
    header_and_title()
    make_table()
    send_email()
    

def background():
    day = -1
    while True:
        time.sleep(4)
        localtime = time.localtime(time.time())
        if(time.localtime(time.time())[6] == 6 and day!=time.localtime(time.time())[2]):
            make_weekly_transaction_email()
            day = time.localtime(time.time())[2]
f = threading.Thread(name='foreground', target=foreground)
b = threading.Thread(name = 'background', target = background)
f.start()
b.start()

localtime = time.localtime(time.time())


