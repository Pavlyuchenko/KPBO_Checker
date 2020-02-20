import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = 'michaelg.pavlicek@gmail.com'
password = 'Amaroon15122002'
send_to_email = 'michaelg.pavlicek@gmail.com'
subject = 'test'
message = 'Lol'
messageHTML = '<h1>THAT\'S AWESOME!!!</h1> <p style="color: red;">I\'m red text</p>'

msg = MIMEMultipart('alternative')
msg['From'] = email
msg['To'] = send_to_email
msg['subject'] = subject

msg.attach(MIMEText(message, 'plain'))
msg.attach(MIMEText(messageHTML, 'html'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
