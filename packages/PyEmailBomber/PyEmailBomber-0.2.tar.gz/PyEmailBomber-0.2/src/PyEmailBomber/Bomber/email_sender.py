
from smtplib import SMTP



class Email:
    
    def __init__(self, sender:str, sender_password : str):
        self.__sender = sender
        self.__sender_password = sender_password
    
    def send_email(self, receiver : str, message : str, subject : str):

        self.__receiver = receiver
        self.__message = message
        self.__subject = subject

        # Log in to server using secure context and send email
        #context = ssl.create_default_context()

        msg1 = 'Subject: %s\n\n%s' % (self.__subject, self.__message)
        server = SMTP("smtp.gmail.com",587)
        server.starttls()
        try:
            server.login(self.__sender, self.__sender_password)
        except:
            print("")
            print("""check for the following:
            1. Read prerequisite section 
            2. Check app password
            3. try again and enter details carefully
            """)
            return False
        else:
            server.sendmail(from_addr= self.__sender,to_addrs= self.__receiver,msg= msg1)
            server.close()
            return True
    
    def email_bomber(self, receivers:list[str], message:str, subject : str, count:int, time_lapse:int):
        from time import sleep
        for i in receivers:
            temp = subject
            for j in range(count):
                temp = temp + str(j)
                self.send_email(i, message=message, subject=temp)
                print('Email sent to', i, '\tcount -> ', j+1)
                sleep(time_lapse)
            temp = subject

            