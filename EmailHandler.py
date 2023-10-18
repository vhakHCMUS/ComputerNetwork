import imaplib
import email
import smtplib
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL = "networkdummy2023@gmail.com"
PASSWORD = "icin ujtn kyfa oyje"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

class EmailHandler():
    def __init__(self):
        self.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        self.mail.login(EMAIL, PASSWORD)
    def readLastestEmail(self):
        self.mail.select("inbox")

        _, data = self.mail.search(None, "UNSEEN")
        mail_ids = data[0].split()
        
        subject = content = "EMPTY"
        if not mail_ids:
            return subject, content

        latest_email_id = int(mail_ids[-1])

        _, data = self.mail.fetch(str(latest_email_id), "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject if encoding is None else subject.decode(encoding)

        content = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                content += body.decode("utf-8")

        #make sender the email address of the sender
        sender = msg["From"].split()[-1].strip("<>")
        return subject, content, sender
    
    def sendMail(self, to, subject, content = '', imageAttach = None):
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg["To"] = to
        html = '''\
            <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css">
                    <style>
                    table {
                        margin: 0 auto;
                        border-collapse: collapse;
                        border-spacing: 0;
                        width: 100%;
                        border: 1px solid #ddd;
                    }
                    tr,td {
                        padding: 5px
                    }
                    </style>
                </head>

                <body>
                    <div class="e-mail"style="background-color: #bfb8ad; padding: 10px " >
                        <div class="container ">
                            <div class ="inner-wrap" style="background: white; padding: 10px ">
                                <div class="row"></div>
                                    <div class="col-xl-12" style="background-color: white; text-align:  left;">
                                        <div>
                                            <img src="https://i.imgur.com/VFEtJYz.png" height="60" width="250"/>
                                        </div>
                                        <hr>
                                        <div class="title" style="text-align: center;">
                                            <h1>Remote control by Email</h1>
                                            <p>
            '''
        html += subject
        html += '''
                                            </p>
                                        </div>

                                        <hr>

                                        <div class="content" style="position: relative;">
                                            <p>
            '''
        html += content
        if imageAttach is not None:
            html += '''<div style="text-align: center;"><br> <img src="cid:image" height="500" padding="20"/></div> <br> '''
        html += '''
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <p style="text-align: center;">
                                    <br><br>
                                    fit@hcmus <br>
                                    This project is built by students from 22CLC02 for the Computer Network (CSC10008) course. <br>
                                    More information can be found <a href="https://github.com/vhakHCMUS/ComputerNetwork">here</a>. <br>
                                    If you need any support, please send an email to nhminh22@fitus.edu.vn
                                </p>
                            </div>
                        </div>
                    </div>
                </body>

                </html>
        '''
        htmlRead = MIMEText(html, 'html')
        msg.attach(htmlRead)
        if imageAttach is not None:
            with open(imageAttach, 'rb') as file:
                image = MIMEImage(file.read())
                image.add_header('Content-ID','image')
                msg.attach(image)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()