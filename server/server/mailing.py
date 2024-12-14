import smtplib
from email.mime.text import MIMEText

# sending a message to an email
def mailing(login: str, password: str, 
            topic: str, mail_text: str,
            users: list):
    
    print('pre ok')
    sender = login
    password = password
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    print('fnc Ok')

    try:
        server.login(sender, password)
        print('Mailing ok')
        msg = MIMEText(mail_text)
        msg["Subject"] = topic

        for i in users:
            server.sendmail(sender, i, msg.as_string())
        return 'Success'
    
    except Exception as _ex:
        return f'Server error, invalid login or password'

    
