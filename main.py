import EmailHandler as em
import KeyLogger as keyl
import ListApp as app
import ListProcess as proc
import ScreenShot
import Power
import socket

# Host a server to read the data from email
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8080))
s.listen()


print("Server listening on port 8080...")


# Main loop
em = em.EmailHandler()
while True:
    emailData = em.read_emails()

    order = emailData[1]
    print(order)
