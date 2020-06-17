from flask import *
from flask import Flask, render_template
from joblib import load
from bs4 import BeautifulSoup
import requests
from itertools import groupby
import logging
import pandas as pd
import smtplib
import json
import numpy as np




# initialize logging 
LOG_FILE_NAME= 'log.txt'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s''',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE_NAME,
                    filemode='w')




app = Flask(__name__) #create instence of web server


appstock = load('deployFile.joblib')
acnstock = load('ACN.joblib')
infystock = load('INFY.joblib')
orclstock = load('ORCL.joblib')
ctshstock = load('CTSH.joblib')

@app.route('/',methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/menu',methods=['POST', 'GET'])
def menu():
    return render_template('menu.html')

@app.route('/CTSH',methods=['POST', 'GET'])
def ctsh():
    url_NIFTY='https://in.finance.yahoo.com/quote/%5ENSEI?p=^NSEI'
    url_Nasdaq = 'https://in.finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    url_HangSeng = 'https://in.finance.yahoo.com/quote/%5EHSI?p=^HSI'
    url_Nikkei = 'https://in.finance.yahoo.com/quote/%5EN225?p=^N225'
    url_estrain = 'https://in.finance.yahoo.com/quote/ESCORTS.NS?p=ESCORTS.NS&.tsrc=fin-srch'
    url_CTSH = 'https://in.finance.yahoo.com/quote/CTSH?p=CTSH&.tsrc=fin-srch'
    response1 = requests.get(url_NIFTY)
    response2 = requests.get(url_Nasdaq)
    response3 = requests.get(url_HangSeng)
    response4 = requests.get(url_Nikkei)
    response5 = requests.get(url_estrain)
    response6 = requests.get(url_CTSH)
    soup = BeautifulSoup(response1.text,'html.parser')
    soup2 = BeautifulSoup(response2.text,'html.parser')
    soup3 = BeautifulSoup(response3.text,'html.parser')
    soup4 = BeautifulSoup(response4.text,'html.parser')
    soup5 = BeautifulSoup(response5.text,'html.parser')
    soup6 = BeautifulSoup(response6.text,'html.parser')
    #nifty
    nifty_data = soup.find(id="quote-summary").getText()
    nifty_data = nifty_data.replace(',','')
    nifty_data = nifty_data.split(" ")
    res = [''.join(j).strip() for sub in nifty_data  
            for k, j in groupby(sub, str.isdigit)] 
    NiftyClose = res[2]+res[3]+res[4]
    NiftyOpen = res[6]+res[7]+res[8]
    #nasdaq
    nasdaq_data = soup2.find(id="quote-summary").getText()
    nasdaq_data = nasdaq_data.replace(',','')
    nasdaq_data = nasdaq_data.split(" ")
    res = [''.join(j).strip() for sub in nasdaq_data  
            for k, j in groupby(sub, str.isdigit)] 
    nasdaqClose = res[2]+res[3]+res[4]
    #HangSeng
    HangSeng_data = soup3.find(id="quote-summary").getText()
    HangSeng_data = HangSeng_data.replace(',','')
    HangSeng_data = HangSeng_data.split(" ")
    res = [''.join(j).strip() for sub in HangSeng_data  
            for k, j in groupby(sub, str.isdigit)] 
    HangSengClose = res[2]+res[3]+res[4]
    HangSengOpen = res[6]+res[7]+res[8]
    #Nikkei
    Nikkei_data = soup4.find(id="quote-summary").getText()
    Nikkei_data = Nikkei_data.replace(',','')
    Nikkei_data = Nikkei_data.split(" ")
    res = [''.join(j).strip() for sub in Nikkei_data  
            for k, j in groupby(sub, str.isdigit)] 
    NikkeiClose = res[2]+res[3]+res[4]
    NikkeiOpen = res[6]+res[7]+res[8]
    #estrain
    estrain_data = soup5.find(id="quote-summary").getText()
    estrain_data = estrain_data.replace(',','')
    estrain_data = estrain_data.split(" ")
    res = [''.join(j).strip() for sub in estrain_data  
            for k, j in groupby(sub, str.isdigit)] 
    estrainClose = res[2]+res[3]+res[4]
    #CTSH
    CTSH_data = soup6.find(id="quote-summary").getText()
    CTSH_data = CTSH_data.replace(',','')
    CTSH_data = CTSH_data.split(" ")
    res = [''.join(j).strip() for sub in CTSH_data
            for k, j in groupby(sub, str.isdigit)] 
    CTSHClose = res[2]+res[3]+res[4]
    
        
    list = ([[HangSengClose,HangSengOpen,nasdaqClose,NikkeiClose,NikkeiOpen,NiftyClose,NiftyOpen,estrainClose,CTSHClose]])
    data = pd.DataFrame(list)
    ctsh_Open = ctshstock.predict(data)
    js = ctsh_Open[0]
    js ={"name":"COGNIZANT OPEN PRICE: ","value":js}
    js2 ={"title":"Cognizant Algorithmic Trading"}
    js3 = {" Hang_Seng_AdjClose_ : ":HangSengClose,"  Hang_Seng_Open : ":HangSengOpen,
           "  NASDAQ_AdjClose_ :":nasdaqClose,"  Nikkei_225_AdjClose_ : ":NikkeiClose,
           "  Nikkei_225_Open : ":NikkeiOpen,"  NIFTY_50_AdjClose_ : ":NiftyClose,
           "  NIFTY_50_Open_ : ":NiftyOpen,"  Escort_AdjClose_ :":estrainClose,
           "  Cognizant_AdjClose : ":CTSHClose}
    js = json.dumps(js)
    js = json.loads(js)
    js2 = json.dumps(js2)
    js2 = json.loads(js2)
    js3 = json.dumps(js3)
    js3 = json.loads(js3)

    # ***********************enter your email details******************************* 
   # ob=smtplib.SMTP('smtp.gmail.com',587)
   # ob.starttls()
   # ob.login('Sender Email','Sender password')
   # subject='Your prediction result'
   # body = "Open Price of Escorts stock : ",result
   # message="Subject:{}\n\n{}".format(subject,body)
   # list= ['List of emails need to get result']
   # ob.sendmail("Sender email",list,message)
   # ob.quit()
   # msg = "Prediction Result is sended to these Email addresses:",list
   # return render_template('Autoprd.html',result=result,msg=msg)
    return render_template('INFY.html',result=js,data=js3,title=js2)
    
@app.route('/ORCL',methods=['POST', 'GET'])
def orcl():
    url_NIFTY='https://in.finance.yahoo.com/quote/%5ENSEI?p=^NSEI'
    url_Nasdaq = 'https://in.finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    url_HangSeng = 'https://in.finance.yahoo.com/quote/%5EHSI?p=^HSI'
    url_Nikkei = 'https://in.finance.yahoo.com/quote/%5EN225?p=^N225'
    url_estrain = 'https://in.finance.yahoo.com/quote/ESCORTS.NS?p=ESCORTS.NS&.tsrc=fin-srch'
    url_ORCL = 'https://in.finance.yahoo.com/quote/ORCL?p=ORCL&.tsrc=fin-srch'
    response1 = requests.get(url_NIFTY)
    response2 = requests.get(url_Nasdaq)
    response3 = requests.get(url_HangSeng)
    response4 = requests.get(url_Nikkei)
    response5 = requests.get(url_estrain)
    response6 = requests.get(url_ORCL)
    soup = BeautifulSoup(response1.text,'html.parser')
    soup2 = BeautifulSoup(response2.text,'html.parser')
    soup3 = BeautifulSoup(response3.text,'html.parser')
    soup4 = BeautifulSoup(response4.text,'html.parser')
    soup5 = BeautifulSoup(response5.text,'html.parser')
    soup6 = BeautifulSoup(response6.text,'html.parser')
    #nifty
    nifty_data = soup.find(id="quote-summary").getText()
    nifty_data = nifty_data.replace(',','')
    nifty_data = nifty_data.split(" ")
    res = [''.join(j).strip() for sub in nifty_data  
            for k, j in groupby(sub, str.isdigit)] 
    NiftyClose = res[2]+res[3]+res[4]
    NiftyOpen = res[6]+res[7]+res[8]
    #nasdaq
    nasdaq_data = soup2.find(id="quote-summary").getText()
    nasdaq_data = nasdaq_data.replace(',','')
    nasdaq_data = nasdaq_data.split(" ")
    res = [''.join(j).strip() for sub in nasdaq_data  
            for k, j in groupby(sub, str.isdigit)] 
    nasdaqClose = res[2]+res[3]+res[4]
    #HangSeng
    HangSeng_data = soup3.find(id="quote-summary").getText()
    HangSeng_data = HangSeng_data.replace(',','')
    HangSeng_data = HangSeng_data.split(" ")
    res = [''.join(j).strip() for sub in HangSeng_data  
            for k, j in groupby(sub, str.isdigit)] 
    HangSengClose = res[2]+res[3]+res[4]
    HangSengOpen = res[6]+res[7]+res[8]
    #Nikkei
    Nikkei_data = soup4.find(id="quote-summary").getText()
    Nikkei_data = Nikkei_data.replace(',','')
    Nikkei_data = Nikkei_data.split(" ")
    res = [''.join(j).strip() for sub in Nikkei_data  
            for k, j in groupby(sub, str.isdigit)] 
    NikkeiClose = res[2]+res[3]+res[4]
    NikkeiOpen = res[6]+res[7]+res[8]
    #estrain
    estrain_data = soup5.find(id="quote-summary").getText()
    estrain_data = estrain_data.replace(',','')
    estrain_data = estrain_data.split(" ")
    res = [''.join(j).strip() for sub in estrain_data  
            for k, j in groupby(sub, str.isdigit)] 
    estrainClose = res[2]+res[3]+res[4]
    #ORCL
    ORCL_data = soup6.find(id="quote-summary").getText()
    ORCL_data = ORCL_data.replace(',','')
    ORCL_data = ORCL_data.split(" ")
    res = [''.join(j).strip() for sub in ORCL_data
            for k, j in groupby(sub, str.isdigit)] 
    ORCLClose = res[2]+res[3]+res[4]
    
        
    list = ([[HangSengClose,HangSengOpen,nasdaqClose,NikkeiClose,NikkeiOpen,NiftyClose,NiftyOpen,estrainClose,ORCLClose]])
    data = pd.DataFrame(list)
    orcl_Open = orclstock.predict(data)
    js = orcl_Open[0]
    js ={"name":"ORACLE OPEN PRICE: ","value":js}
    js2 ={"title":"Oracle Algorithmic Trading"}
    js3 = {" Hang_Seng_AdjClose_ : ":HangSengClose,"  Hang_Seng_Open : ":HangSengOpen,
           "  NASDAQ_AdjClose_ :":nasdaqClose,"  Nikkei_225_AdjClose_ : ":NikkeiClose,
           "  Nikkei_225_Open : ":NikkeiOpen,"  NIFTY_50_AdjClose_ : ":NiftyClose,
           "  NIFTY_50_Open_ : ":NiftyOpen,"  Escort_AdjClose_ :":estrainClose,
           "  Oracle_AdjClose_ : ":ORCLClose}
    js = json.dumps(js)
    js = json.loads(js)
    js2 = json.dumps(js2)
    js2 = json.loads(js2)
    js3 = json.dumps(js3)
    js3 = json.loads(js3)
    # ***********************enter your email details******************************* 
   # ob=smtplib.SMTP('smtp.gmail.com',587)
   # ob.starttls()
   # ob.login('Sender Email','Sender password')
   # subject='Your prediction result'
   # body = "Open Price of Escorts stock : ",result
   # message="Subject:{}\n\n{}".format(subject,body)
   # list= ['List of emails need to get result']
   # ob.sendmail("Sender email",list,message)
   # ob.quit()
   # msg = "Prediction Result is sended to these Email addresses:",list
   # return render_template('Autoprd.html',result=result,msg=msg)
    return render_template('INFY.html',result=js,data=js3,title=js2)

    

@app.route('/INFY',methods=['POST', 'GET'])
def infy():
    url_NIFTY='https://in.finance.yahoo.com/quote/%5ENSEI?p=^NSEI'
    url_Nasdaq = 'https://in.finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    url_HangSeng = 'https://in.finance.yahoo.com/quote/%5EHSI?p=^HSI'
    url_Nikkei = 'https://in.finance.yahoo.com/quote/%5EN225?p=^N225'
    url_estrain = 'https://in.finance.yahoo.com/quote/ESCORTS.NS?p=ESCORTS.NS&.tsrc=fin-srch'
    url_INFY = 'https://in.finance.yahoo.com/quote/INFY?p=INFY&.tsrc=fin-srch'
    response1 = requests.get(url_NIFTY)
    response2 = requests.get(url_Nasdaq)
    response3 = requests.get(url_HangSeng)
    response4 = requests.get(url_Nikkei)
    response5 = requests.get(url_estrain)
    response6 = requests.get(url_INFY)
    soup = BeautifulSoup(response1.text,'html.parser')
    soup2 = BeautifulSoup(response2.text,'html.parser')
    soup3 = BeautifulSoup(response3.text,'html.parser')
    soup4 = BeautifulSoup(response4.text,'html.parser')
    soup5 = BeautifulSoup(response5.text,'html.parser')
    soup6 = BeautifulSoup(response6.text,'html.parser')
    #nifty
    nifty_data = soup.find(id="quote-summary").getText()
    nifty_data = nifty_data.replace(',','')
    nifty_data = nifty_data.split(" ")
    res = [''.join(j).strip() for sub in nifty_data  
            for k, j in groupby(sub, str.isdigit)] 
    NiftyClose = res[2]+res[3]+res[4]
    NiftyOpen = res[6]+res[7]+res[8]
    #nasdaq
    nasdaq_data = soup2.find(id="quote-summary").getText()
    nasdaq_data = nasdaq_data.replace(',','')
    nasdaq_data = nasdaq_data.split(" ")
    res = [''.join(j).strip() for sub in nasdaq_data  
            for k, j in groupby(sub, str.isdigit)] 
    nasdaqClose = res[2]+res[3]+res[4]
    #HangSeng
    HangSeng_data = soup3.find(id="quote-summary").getText()
    HangSeng_data = HangSeng_data.replace(',','')
    HangSeng_data = HangSeng_data.split(" ")
    res = [''.join(j).strip() for sub in HangSeng_data  
            for k, j in groupby(sub, str.isdigit)] 
    HangSengClose = res[2]+res[3]+res[4]
    HangSengOpen = res[6]+res[7]+res[8]
    #Nikkei
    Nikkei_data = soup4.find(id="quote-summary").getText()
    Nikkei_data = Nikkei_data.replace(',','')
    Nikkei_data = Nikkei_data.split(" ")
    res = [''.join(j).strip() for sub in Nikkei_data  
            for k, j in groupby(sub, str.isdigit)] 
    NikkeiClose = res[2]+res[3]+res[4]
    NikkeiOpen = res[6]+res[7]+res[8]
    #estrain
    estrain_data = soup5.find(id="quote-summary").getText()
    estrain_data = estrain_data.replace(',','')
    estrain_data = estrain_data.split(" ")
    res = [''.join(j).strip() for sub in estrain_data  
            for k, j in groupby(sub, str.isdigit)] 
    estrainClose = res[2]+res[3]+res[4]
    #INFY
    INFY_data = soup6.find(id="quote-summary").getText()
    INFY_data = INFY_data.replace(',','')
    INFY_data = INFY_data.split(" ")
    res = [''.join(j).strip() for sub in INFY_data
            for k, j in groupby(sub, str.isdigit)] 
    INFYClose = res[2]+res[3]+res[4]
    
        
    list = ([[HangSengClose,HangSengOpen,nasdaqClose,NikkeiClose,NikkeiOpen,NiftyClose,NiftyOpen,estrainClose,INFYClose]])
    data = pd.DataFrame(list)
    infy_Open = infystock.predict(data)
    js = infy_Open[0]
    js ={"name":"INFOSYS OPEN PRICE: ","value":js}
    js2 ={"title":"Infosys Algorithmic Trading"}
    js3 = {"Hang_Seng_AdjClose_ : ":HangSengClose,"  Hang_Seng_Open : ":HangSengOpen,
           "  NASDAQ_AdjClose_ :":nasdaqClose,"  Nikkei_225_AdjClose_ : ":NikkeiClose,
           "  Nikkei_225_Open : ":NikkeiOpen,"  NIFTY_50_AdjClose_ : ":NiftyClose,
           "  NIFTY_50_Open : ":NiftyOpen,"  Escort_AdjClose_ :":estrainClose,
           "  Infosys_AdjClose_ : ":INFYClose}
    js = json.dumps(js)
    js = json.loads(js)
    js2 = json.dumps(js2)
    js2 = json.loads(js2)
    js3 = json.dumps(js3)
    js3 = json.loads(js3)
    # ***********************enter your email details******************************* 
   # ob=smtplib.SMTP('smtp.gmail.com',587)
   # ob.starttls()
   # ob.login('Sender Email','Sender password')
   # subject='Your prediction result'
   # body = "Open Price of Escorts stock : ",result
   # message="Subject:{}\n\n{}".format(subject,body)
   # list= ['List of emails need to get result']
   # ob.sendmail("Sender email",list,message)
   # ob.quit()
   # msg = "Prediction Result is sended to these Email addresses:",list
   # return render_template('Autoprd.html',result=result,msg=msg) 
    return render_template('INFY.html',result=js,data=js3,title=js2)

@app.route('/ACN',methods=['POST', 'GET'])
def acn():
    url_NIFTY='https://in.finance.yahoo.com/quote/%5ENSEI?p=^NSEI'
    url_Nasdaq = 'https://in.finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    url_HangSeng = 'https://in.finance.yahoo.com/quote/%5EHSI?p=^HSI'
    url_Nikkei = 'https://in.finance.yahoo.com/quote/%5EN225?p=^N225'
    url_estrain = 'https://in.finance.yahoo.com/quote/ESCORTS.NS?p=ESCORTS.NS&.tsrc=fin-srch'
    url_ACN = 'https://in.finance.yahoo.com/quote/ACN?p=ACN&.tsrc=fin-srch'
    response1 = requests.get(url_NIFTY)
    response2 = requests.get(url_Nasdaq)
    response3 = requests.get(url_HangSeng)
    response4 = requests.get(url_Nikkei)
    response5 = requests.get(url_estrain)
    response6 = requests.get(url_ACN)
    soup = BeautifulSoup(response1.text,'html.parser')
    soup2 = BeautifulSoup(response2.text,'html.parser')
    soup3 = BeautifulSoup(response3.text,'html.parser')
    soup4 = BeautifulSoup(response4.text,'html.parser')
    soup5 = BeautifulSoup(response5.text,'html.parser')
    soup6 = BeautifulSoup(response6.text,'html.parser')
    #nifty
    nifty_data = soup.find(id="quote-summary").getText()
    nifty_data = nifty_data.replace(',','')
    nifty_data = nifty_data.split(" ")
    res = [''.join(j).strip() for sub in nifty_data  
            for k, j in groupby(sub, str.isdigit)] 
    NiftyClose = res[2]+res[3]+res[4]
    NiftyOpen = res[6]+res[7]+res[8]
    #nasdaq
    nasdaq_data = soup2.find(id="quote-summary").getText()
    nasdaq_data = nasdaq_data.replace(',','')
    nasdaq_data = nasdaq_data.split(" ")
    res = [''.join(j).strip() for sub in nasdaq_data  
            for k, j in groupby(sub, str.isdigit)] 
    nasdaqClose = res[2]+res[3]+res[4]
    #HangSeng
    HangSeng_data = soup3.find(id="quote-summary").getText()
    HangSeng_data = HangSeng_data.replace(',','')
    HangSeng_data = HangSeng_data.split(" ")
    res = [''.join(j).strip() for sub in HangSeng_data  
            for k, j in groupby(sub, str.isdigit)] 
    HangSengClose = res[2]+res[3]+res[4]
    HangSengOpen = res[6]+res[7]+res[8]
    #Nikkei
    Nikkei_data = soup4.find(id="quote-summary").getText()
    Nikkei_data = Nikkei_data.replace(',','')
    Nikkei_data = Nikkei_data.split(" ")
    res = [''.join(j).strip() for sub in Nikkei_data  
            for k, j in groupby(sub, str.isdigit)] 
    NikkeiClose = res[2]+res[3]+res[4]
    NikkeiOpen = res[6]+res[7]+res[8]
    #estrain
    estrain_data = soup5.find(id="quote-summary").getText()
    estrain_data = estrain_data.replace(',','')
    estrain_data = estrain_data.split(" ")
    res = [''.join(j).strip() for sub in estrain_data  
            for k, j in groupby(sub, str.isdigit)] 
    estrainClose = res[2]+res[3]+res[4]
    #Accenture
    ACN_data = soup6.find(id="quote-summary").getText()
    ACN_data = ACN_data.replace(',','')
    ACN_data = ACN_data.split(" ")
    res = [''.join(j).strip() for sub in ACN_data
            for k, j in groupby(sub, str.isdigit)] 
    ACNClose = res[2]+res[3]+res[4]
    
    list = ([[HangSengClose,HangSengOpen,nasdaqClose,NikkeiClose,NikkeiOpen,NiftyClose,NiftyOpen,estrainClose,ACNClose]])
    data = pd.DataFrame(list)
    acn_Open = acnstock.predict(data)
    js = acn_Open[0]
    js ={"name":"ACCENTURE OPEN PRICE: ","value":js}
    js2 ={"title":"Accenture Algorithmic Trading"}
    js3 = {" Hang_Seng_AdjClose_ : ":HangSengClose,"  Hang_Seng_Open : ":HangSengOpen,
           "  NASDAQ_AdjClose_ :":nasdaqClose,"  Nikkei_225_AdjClose_ : ":NikkeiClose,
           "  Nikkei_225_Open : ":NikkeiOpen,"  NIFTY_50_AdjClose_ : ":NiftyClose,
           "  NIFTY_50_Open_ : ":NiftyOpen,"  Escort_AdjClose_ :":estrainClose,
           "  Accenture_AdjClose : ":ACNClose}
    js = json.dumps(js)
    js = json.loads(js)
    js2 = json.dumps(js2)
    js2 = json.loads(js2)
    js3 = json.dumps(js3)
    js3 = json.loads(js3)

    # ***********************enter your email details******************************* 
   # ob=smtplib.SMTP('smtp.gmail.com',587)
   # ob.starttls()
   # ob.login('Sender Email','Sender password')
   # subject='Your prediction result'
   # body = "Open Price of Escorts stock : ",result
   # message="Subject:{}\n\n{}".format(subject,body)
   # list= ['List of emails need to get result']
   # ob.sendmail("Sender email",list,message)
   # ob.quit()
   # msg = "Prediction Result is sended to these Email addresses:",list
   # return render_template('Autoprd.html',result=result,msg=msg) 
    return render_template('INFY.html',result=js,data=js3,title=js2)
    
    
@app.route('/auto',methods=['POST', 'GET'])
def auto():
    url_NIFTY='https://in.finance.yahoo.com/quote/%5ENSEI?p=^NSEI'
    url_Nasdaq = 'https://in.finance.yahoo.com/quote/%5EIXIC?p=^IXIC'
    url_HangSeng = 'https://in.finance.yahoo.com/quote/%5EHSI?p=^HSI'
    url_Nikkei = 'https://in.finance.yahoo.com/quote/%5EN225?p=^N225'
    url_estrain = 'https://in.finance.yahoo.com/quote/ESCORTS.NS?p=ESCORTS.NS&.tsrc=fin-srch'
    response1 = requests.get(url_NIFTY)
    response2 = requests.get(url_Nasdaq)
    response3 = requests.get(url_HangSeng)
    response4 = requests.get(url_Nikkei)
    response5 = requests.get(url_estrain)
    soup = BeautifulSoup(response1.text,'html.parser')
    soup2 = BeautifulSoup(response2.text,'html.parser')
    soup3 = BeautifulSoup(response3.text,'html.parser')
    soup4 = BeautifulSoup(response4.text,'html.parser')
    soup5 = BeautifulSoup(response5.text,'html.parser')
    #nifty
    nifty_data = soup.find(id="quote-summary").getText()
    nifty_data = nifty_data.replace(',','')
    nifty_data = nifty_data.split(" ")
    res = [''.join(j).strip() for sub in nifty_data  
            for k, j in groupby(sub, str.isdigit)] 
    NiftyClose = res[2]+res[3]+res[4]
    NiftyOpen = res[6]+res[7]+res[8]
    #nasdaq
    nasdaq_data = soup2.find(id="quote-summary").getText()
    nasdaq_data = nasdaq_data.replace(',','')
    nasdaq_data = nasdaq_data.split(" ")
    res = [''.join(j).strip() for sub in nasdaq_data  
            for k, j in groupby(sub, str.isdigit)] 
    nasdaqClose = res[2]+res[3]+res[4]
    #HangSeng
    HangSeng_data = soup3.find(id="quote-summary").getText()
    HangSeng_data = HangSeng_data.replace(',','')
    HangSeng_data = HangSeng_data.split(" ")
    res = [''.join(j).strip() for sub in HangSeng_data  
            for k, j in groupby(sub, str.isdigit)] 
    HangSengClose = res[2]+res[3]+res[4]
    HangSengOpen = res[6]+res[7]+res[8]
    #Nikkei
    Nikkei_data = soup4.find(id="quote-summary").getText()
    Nikkei_data = Nikkei_data.replace(',','')
    Nikkei_data = Nikkei_data.split(" ")
    res = [''.join(j).strip() for sub in Nikkei_data  
            for k, j in groupby(sub, str.isdigit)] 
    NikkeiClose = res[2]+res[3]+res[4]
    NikkeiOpen = res[6]+res[7]+res[8]
    #estrain
    estrain_data = soup5.find(id="quote-summary").getText()
    estrain_data = estrain_data.replace(',','')
    estrain_data = estrain_data.split(" ")
    res = [''.join(j).strip() for sub in estrain_data  
            for k, j in groupby(sub, str.isdigit)] 
    estrainClose = res[2]+res[3]+res[4]
    list = ([[HangSengClose,HangSengOpen,nasdaqClose,NikkeiClose,NikkeiOpen,NiftyClose,NiftyOpen,estrainClose]])
    data = pd.DataFrame(list)
    es_train_Open = appstock.predict(data)
    js = es_train_Open[0]
    js ={"name":"ESCORT OPEN PRICE: ","value":js}
    js2 ={"title":"Escort Algorithmic Trading"}
    js3 = {" Hang_Seng_AdjClose_ : ":HangSengClose,"  Hang_Seng_Open : ":HangSengOpen,
           "  NASDAQ_AdjClose_ :":nasdaqClose,"  Nikkei_225_AdjClose_ : ":NikkeiClose,
           "  Nikkei_225_Open : ":NikkeiOpen,"  NIFTY_50_AdjClose_ : ":NiftyClose,
           "  NIFTY_50_Open_ : ":NiftyOpen,"  Escort_AdjClose_ :":estrainClose,
           "  Escort_AdjClose_ : ":estrainClose}
    js = json.dumps(js)
    js = json.loads(js)
    js2 = json.dumps(js2)
    js2 = json.loads(js2)
    js3 = json.dumps(js3)
    js3 = json.loads(js3)

    # ***********************enter your email details******************************* 
    
   # ob=smtplib.SMTP('smtp.gmail.com',587)
   # ob.starttls()
   # ob.login('Sender Email','Sender password')
   # subject='Your prediction result'
   # body = "Open Price of Escorts stock : ",result
   # message="Subject:{}\n\n{}".format(subject,body)
   # list= ['List of emails need to get result']
   # ob.sendmail("Sender email",list,message)
   # ob.quit()
   # msg = "Prediction Result is sended to these Email addresses:",list
   # return render_template('Autoprd.html',result=result,msg=msg)
    return render_template('INFY.html',result=js,data=js3,title=js2)
              
    
if __name__ == '__main__': #this only page run as a main page if it not run as a main page web server will not work,
    app.run()