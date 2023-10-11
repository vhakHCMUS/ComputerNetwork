import imaplib
import socket
import email
from Feature import *

from email.header import decode_header

# Thay đổi giá trị này cho Gmail
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993  # Sử dụng cổng IMAPS (SSL/TLS) của Gmail
EMAIL = "your_email@gmail.com"  # Địa chỉ email Gmail
PASSWORD = "your_password"  # Mật khẩu email Gmail

def read_emails():
    # Kết nối đến máy chủ IMAP Gmail
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)

    # Chọn hộp thư đến
    mail.select("inbox")

    # Tìm tất cả email trong hộp thư
    result, data = mail.search(None, "ALL")

    if result == "OK":
        email_ids = data[0].split()
        for email_id in email_ids:
            # Lấy email theo ID
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            if result == "OK":
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Lấy tiêu đề email
                subject, encoding = decode_header(msg["Subject"])[0]
                if encoding is not None:
                    subject = subject.decode(encoding)

                # Lấy người gửi email
                from_, encoding = decode_header(msg.get("From"))[0]
                if encoding is not None:
                    from_ = from_.decode(encoding)

                print("From:", from_)
                print("Subject:", subject)
                print("Body:")
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        print(body.decode("utf-8"))

    mail.logout()

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()


    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.send(b"Hello! This is the email server. What would you like to do?")
        data = client_socket.recv(1024)
        if data == b"READ_EMAILS":
            print("Client requested to read emails.")
            read_emails()
        client_socket.close()
