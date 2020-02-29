from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
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




def get_books_from_file():
    books = {}

    file = open('C:\\Users\\Michal\\Desktop\\books.txt', 'r')

    for line in file:
        books[line.split(':')[0]] = line.split(':')[1] + ":" + line.split(':')[2]
    return books


def remove_book_from_file(book):
    books = {}

    file = open('C:\\Users\\Michal\\Desktop\\books.txt', 'r')

    for line in file:
        if not line.split(":")[0] == book:
            books[line.split(':')[0]] = line.split(':')[1] + ":" + line.split(':')[2]

    file.close()

    file = open('C:\\Users\\Michal\\Desktop\\books.txt', 'w')
    for i, j in books.items():
        file.write(i + ":" + j)

remove_book_from_file('Jméno větru')


wanted_books = get_books_from_file()

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path="C:\\Users\\Michal\\Desktop\\geckodriver.exe", options=options)

print("Starting geckodriver.exe (Firefox)...")

for book in wanted_books.keys():
    ordered = False
    driver.get(wanted_books[book])  # Choose each book from dictionary
    table_rows = driver.find_elements_by_xpath('//tr')  # Find ALL table row elements
    potentional_free_books = []  # List for books in Dospělí, Mládež and Kateřinky
    for i in table_rows:  # For each table row
        try:
            valid = i.find_element_by_class_name('SVSL1')  # If you find table row that stands for some oddělení
            valid = ''.join([i for i in valid.text if not i.isdigit()]).replace("  ", " ").replace(".", "")
            if valid == " " or valid == "  " or valid == " M/III " or valid == " KA " or valid == " BIS ":  # Then check if it is one of my possible oddělení
                potentional_free_books.append(i)  # If the two upper conditions are met, add it to the List
        except:
            pass

    for i in potentional_free_books:  # For each potential free book
        try:
            i.find_elements_by_tag_name('td')[4].click()  # Try to click 'objednat odložení'
            driver.find_element_by_id('CC').send_keys('17753')  # Username
            driver.find_element_by_id('RC').send_keys('751115')  # Password

            driver.find_element_by_id('RC').send_keys(Keys.ENTER)  # Confirm
            print("\n" + book + " was ordered. \n")
            ordered = True
            send_email(book)
            remove_book_from_file(book)
            break
        except:  # Second try, for special reason: The td might be on another index
            try:
                i.find_elements_by_tag_name('td')[3].click()  # Try to click 'objednat odložení'
                driver.find_element_by_id('CC').send_keys('17753')  # Username
                driver.find_element_by_id('RC').send_keys('751115')  # Password

                driver.find_element_by_id('RC').send_keys(Keys.ENTER)
                print("\n" + book + " was ordered. \n")
                send_email(book)
                remove_book_from_file(book)
                ordered = True
                break
            except:
                pass
    if not ordered:
        print(book + " is not available")

driver.close()
print("Process finished")
