
from smtplib import SMTP
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    
    def __init__(self, sender:str, sender_password : str):
        self.__sender = sender
        self.__sender_password = sender_password
    
    def send_email(self, receiver : str, message : str, subject : str, filename = None):

        self.__receiver = receiver
        self.__message = message
        self.__subject = subject

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.__sender
        message["To"] = self.__receiver
        message["Subject"] = self.__subject
        message["Bcc"] = self.__receiver  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(self.__message, "plain"))
        if filename is not None:
            filename = filename  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            
        else:
            text = message.as_string()

        # Log in to server using secure context and send email
        #context = ssl.create_default_context()

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
            server.sendmail(from_addr= self.__sender,to_addrs= self.__receiver,msg= text)
            server.close()
            return True
    
    def email_bomber(self, receivers:list[str], message:str, subject : str, count:int, time_lapse:int):
        from time import sleep
        for i in receivers:
            for j in range(count):
                self.send_email(i, message=message, subject=subject)
                print('Email sent to', i, '\tcount -> ', j+1)
                sleep(time_lapse)

            