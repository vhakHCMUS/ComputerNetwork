import csv

class MailList():
    def __init__(self):
        self.data = []
        with open("mails.csv","r") as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                self.data.extend([line])
    def findMail(self, email):
        if(email in self.data):
            return True
        return False
    def addMail(self, email):
        if(email == "" or email in self.data or '@' not in email or '.' not in email or email.find('@') >= email.find('.')):
            return
        self.data.append(email)
        print("new mail added: ", email)
        with open('mails.csv', 'a', newline='') as file:
            csv.writer(file).writerow([email])
