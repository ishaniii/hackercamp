import pymysql
import config
from tv_series import Tv_series
from  mailupdate import MailUpdate
import re

db = pymysql.connect(config.DB_HOST,config.DB_USER,config.DB_PASS,config.DB_NAME)   # Open database connection
cursor = db.cursor()

sql = """CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL AUTO_INCREMENT,
   email_id  CHAR(50) NOT NULL,
   mail_status INT NOT NULL DEFAULT '0',
   PRIMARY KEY (`user_id`))"""              # Create first table as per requirement
    #mail_status = 0 => NOT MAILED YET || mail_status = 1 => MAIL SENT
cursor.execute(sql)

sql2 = """CREATE TABLE IF NOT EXISTS user_series (
    user_id INT NOT NULL,
   series_name  CHAR(50) NOT NULL,
   PRIMARY KEY (`user_id`,`series_name`))"""   # Create second table as per requirement
   # cannot hold duplicate values of series for same user
cursor.execute(sql2)

def isValidEmail(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def main():
    mail_obj = MailUpdate()
    n = int(input("Number of users:" ))
    for i in range(0,n):
        email = input("Email Address: ")
        series_str = input("TV Series: ")
        validity = isValidEmail(email)
        if validity == True :        #check is email id is valid
            series_list = [series_list.strip() for series_list in series_str.split(',')]
            slen = len(series_list)
            query1 = "INSERT INTO users(email_id) VALUES (%s)"
            cursor.execute(query1,(email,))
            user_id = cursor.lastrowid
            str = ""
            for i in range (0,slen):
                str+= " ({},'{}')".format(user_id,series_list[i])
                if i!= slen-1:
                    str+= ","
                series_obj = Tv_series(email,series_list[i])
                mail_obj.add_mail_content(series_obj.name_text,series_obj.status_text)
            query2 = "INSERT INTO user_series(user_id,series_name) VALUES{}"
            cursor.execute(query2.format(str))
        else:
            print("Invalid email address.")
            return
        mail_status = mail_obj.sendmail(email)
        if mail_status == True :                #update mail status in database
            query3 = "UPDATE users SET mail_status = 1 WHERE user_id = {}"
            cursor.execute(query3.format(user_id))
    db.commit()
    db.close()          # disconnect from server

if __name__ == '__main__':
    main()
