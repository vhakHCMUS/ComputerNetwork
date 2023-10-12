import imaplib
import email
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL = "networkdummy2023@gmail.com"
PASSWORD = "icin ujtn kyfa oyje"

class EmailHandler():
    def __init__(self):
        self.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        self.mail.login(EMAIL, PASSWORD)
    def read_emails(self):
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

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                content += body.decode("utf-8")

        return subject, content

    
