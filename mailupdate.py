import smtplib
import config

class MailUpdate:
    server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
    msg = ""

    def add_mail_content(self,name,status):
        self.msg += name+status

    def sendmail(self,receiver_id):
        try:
            self.server.starttls()
            self.server.login(config.SENDER_ID,config.SENDER_PASSWORD)
            self.server.ehlo()
            self.server.sendmail(config.SENDER_ID, receiver_id, self.msg)
            return True
        except smtplib.SMTPException as e:
            print(e)
            return False
