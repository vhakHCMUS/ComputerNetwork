import imaplib
import email
import smtplib
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

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
    
    def sendEmail(self, to, subject, content):
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        content = MIMEText(content.encode("utf-8"), 'plain', 'UTF-8')
        msg.attach(content)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()

    def sendPicture(self, to, subject, filename):
        # Create a MIME object for the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to
        msg["Subject"] = subject

        # Attempt to determine the script directory
        script_directory = os.path.dirname(os.path.abspath(__file__)) if __file__ else ""

        if not script_directory:
            # Handle the case where the script's directory couldn't be determined
            print("Warning: Unable to determine script directory.")
            return

        # Construct the full file path for the image
        full_filename = os.path.join(script_directory, filename)

        # Attach the picture to the email
        with open(full_filename, "rb") as file:
            image = MIMEImage(file.read(), name=os.path.basename(full_filename))
            msg.attach(image)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, msg.as_string())
        server.quit()


    
