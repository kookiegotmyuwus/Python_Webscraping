def decorator(func):
    def inner(user_name):
        c=0
        import mysql.connector
        mydb = mysql.connector.connect(host='localhost',
                                database='scraping_assgn',
                                user='varsha',
                                password='varsha')

        mycursor = mydb.cursor()
        sql = "SELECT * FROM user WHERE username = '"+user_name+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            c+=1
        if(c>0):
            return func(user_name)
        else:
            return "Username is not in database"
    return inner
@decorator
def func(username):
    return username

print(func("radhikagarg1601"))
print(func("ritvik.jain.52206"))
print(func("varsha"))