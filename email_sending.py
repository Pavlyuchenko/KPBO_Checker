import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# TODO - HTML functions such as h1() to make h1("HEllo") -> <h1>Hello</h1>
def send_email(message, subject='Objednávka knihy', send_to='michaelg.pavlicek@gmail.com'):
    email = 'michaelg.pavlicek@gmail.com'
    password = 'Amaroon15122002'
    send_to_email = send_to
    subject = subject
    header = '<body style="font-weight: 700;"><div style="display: flex; align-items: center;"> <img src="https://kpbo.cz/wp-content/uploads/2015/07/logoheader.png"/> <span style="font-size: 50px; color: #564732;">Knihovna Petra Bezruče Opava</span> </div> <hr>'
    body = '<h3 style="margin-left: 30px; font-size: 24px; color: #564732">Kniha <u>' + message + '</u> byla objednána </h3> <a href="https://www.okpb.cz/Opava/cs/orders" style="margin-left: 30px;background-color: #564732;border: none;color: white; padding: 5px 10px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;">Zkontrolovat Objednávky odložení</a>'
    messageHTML = header + body

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

