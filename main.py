import imaplib
import socket
import email
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL = "mmtnhom@gmail.com"
PASSWORD = "emyeubht"

def read_emails():
    # Đọc email mới nhất chưa đọc trong lúc bật server
    mail.select("inbox")

    _, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()
    
    if not mail_ids:
        return  # Không có email mới nào

    latest_email_id = int(mail_ids[-1])

    _, data = mail.fetch(str(latest_email_id), "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Lấy thông tin từ, tiêu đề và nội dung email
    from_, encoding = decode_header(msg.get("From"))[0]
    subject, encoding = decode_header(msg["Subject"])[0]
    subject = subject if encoding is None else subject.decode(encoding)

    print(f"From: {from_}")
    print(f"Subject: {subject}")
    
    print("Body:")
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            print(body.decode("utf-8"))
    print()

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        read_emails()
