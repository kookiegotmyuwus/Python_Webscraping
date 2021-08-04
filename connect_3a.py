import mysql.connector
mydb = mysql.connector.connect(host='localhost',
                                database='scraping_assgn',
                                user='varsha',
                                password='varsha')
if mydb.is_connected():
    print('Connected to MySQL database')

mycursor=mydb.cursor()
# mycursor.execute("CREATE TABLE user(username VARCHAR(255) NOT NULL)")
c=0
val1=[
    'radhikagarg1601', 
    'ritvik.jain.52206', 
    'rishi.ranjan.54966', 
    'utkarsh.parkhi.1', 
    'anshul.d.sharma.7'
]
mycursor=mydb.cursor()
for x in val1:
    val=[]
    sql="INSERT INTO user(username) VALUES(%s)"
    val.append(x)

    mycursor.execute(sql,val)
    mydb.commit()
    c+=mycursor.rowcount

print(c,"was inserted")


mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x) 

mycursor.execute("SELECT * FROM user")
myresult=mycursor.fetchall()
for x in myresult:
    print(x)