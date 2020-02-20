import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# TODO - HTML functions such as h1() to make h1("HEllo") -> <h1>Hello</h1>
def send_email(subject, message, send_to='michaelg.pavlicek@gmail.com'):
    email = 'michaelg.pavlicek@gmail.com'
    password = 'Amaroon15122002'
    send_to_email = send_to
    subject = subject
    messageHTML = message

    msg = MIMEMultipart('alternative')
    msg['From'] = email
    msg['To'] = send_to_email
    msg['subject'] = subject

    msg.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
