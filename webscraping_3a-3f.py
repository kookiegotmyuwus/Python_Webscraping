from selenium import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options 
from getpass import getpass

import requests
from bs4 import BeautifulSoup
import mysql.connector

import json

def mysqlconnect():
    import mysql.connector
    mydb = mysql.connector.connect(host='localhost',
                            database='scraping_assgn_3e',
                            user='varsha',
                            password='varsha')

    return mydb

def decorator(func):
    def inner(user_name):
        mydb=mysqlconnect()
        mycursor=mydb.cursor()
        sql = "SELECT * FROM user WHERE username = '"+user_name+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        c=0
        for x in myresult:
            c+=1
        if(c>0):
            return True #username exists
        else:
            return False
    return inner

def getsoup(username):
    """uses selenium to get soup"""

    usr=input('Enter Email Id:') 
    pwd=input('Enter Password:')

    driver = webdriver.Firefox()
    driver.get('https://www.facebook.com/')
    sleep(1)

    username_box = driver.find_element_by_id('email')
    username_box.send_keys(usr)
    sleep(1)
    
    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd)

    login_box = driver.find_element_by_name('login')
    login_box.click()

    driver.get("https://m.facebook.com/"+username+"/about")
    next_value = 300
    while next_value<3000: 
        #driver.execute_script("next_value="+next_value";")
        driver.execute_script("window.scrollBy(0,"+str(next_value)+")")
        next_value+=300
        sleep(1)

    # r = requests.get("https://m.facebook.com/"+username+"/about")
    # soup = BeautifulSoup(r.content, 'html5lib')
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    # print(soup.prettify())

    return soup

def getname(username,soup):
    """scrape name"""
    name=soup.find('a',attrs={'class':'_6j_c'}).text
    return name

def getcity(username,soup):
    """scrape city"""
    c = soup.findAll('h4')
    city=""
    for x in range(0,len(c)):
        if(c[x+1].text=="Current town/city"):
            city=c[x].text
            break
        else:
            continue
    return city

def getwork(username,soup):
    """scrape work"""
    w = soup.find('div', attrs={'id':'work'})
    w = w.findAll('span', attrs={'class':'_52jd'})
    work=list()
    for x in range(0,len(w)):
        work.append(w[x].text)
    return work

def fav(username,soup):
    """scrape favourites"""
    f = soup.findAll('span', attrs={'class':'_2w79'})
    fav=list()
    for x in range(0,len(f)):
        fav.append(f[x].text)
    out2=""
    if(len(fav)):
        out2+=str(fav)+"\n"
    else:
        out2+="There are no fav \n"
    return out2

@decorator
def func(username):
    return username

def scrap(username):
    mydb=mysqlconnect()
    mycursor=mydb.cursor()
    # mycursor.execute("CREATE TABLE user(username VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, city VARCHAR(255), work VARCHAR(255),fav VARCHAR(255))")

    if(func(username)==False): #username doesn't exist

        #scrapes data
        soup=getsoup(username)
        name=getname(username,soup)
        city=getcity(username,soup)
        work=getwork(username,soup)
        out=fav(username,soup)

        if(city!=None and work!=None):
            obj1=Person(name,city,work)
        elif(city==None and work!=None):
            obj1=Person(name,"",work)
        elif(work==None and city!=None):
            obj1=Person(name,city,"")
        else:
            obj1=Person(name)
        out=out+obj1.show()
        
        # mycursor.execute("CREATE TABLE user(username VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, city VARCHAR(255), work VARCHAR(255))")
        # store values in database
        
        query = "INSERT INTO user(username,name,city,work) VALUES ('{}','{}','{}','{}');".format(str(username), str(name), str(city), json.dumps(work))
        mycursor.execute(query)
        mydb.commit()

        print(out)
        return out

    else:
        sql = "SELECT * FROM user WHERE username = '"+username+"'"
        mycursor.execute(sql)
        myresult=mycursor.fetchall()
        for x in myresult:
            name=x[1]
            city=x[2]
            work=x[3]

        if(city!=None and work!=None):
            obj1=Person(name,city,work)
        elif(city==None and work!=None):
            obj1=Person(name,"",work)
        elif(work==None and city!=None):
            obj1=Person(name,city,"")
        else:
            obj1=Person(name)

        out1=obj1.show()
        print(out1)
        return out1

class Person:
    def __init__(self,name,city,work=None):
        self.name=name
        if(work!=""):
            self.work=work
        if(city==""):
            self.city="Roorkee"
        else:
            self.city=city

    def show(self):
        str='My name is {} and my current city is {}'.format(self.name,self.city)
        return str

# #test cases
# scrap("rushilv4102")
# scrap("radhikagarg1601")
# scrap("varsharamanu")
# # scrap("Samyak.2303")
scrap("anshul.d.sharma.7")

import unittest
class LearnTest(unittest.TestCase):
    def test_func_1(self):
        a="radhikagarg1601"
        result = scrap(a)
        self.assertEqual(result,"['Quantum Computing Group', 'How I Met Your Mother', 'IITR Honest Confessions', 'The DREAM PIE Bakery', 'IIT Roorkee', 'mansiyogaandfitness']"+"\n"+"My name is Radhika Garg and my current city is Roorkee")
    def test_func_2(self):
        a="anshul.d.sharma.7"
        result = scrap(a)
        self.assertEqual(result,"My name is Anshul Dutt Sharma and my current city is Roorkee")

if __name__=="__main__":
    unittest.main()