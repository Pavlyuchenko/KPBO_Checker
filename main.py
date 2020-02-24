from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import email_sending


def get_books_from_file():
    books = {}

    file = open('books.txt', 'r')

    for line in file:
        books[line.split(':')[0]] = line.split(':')[1] + ":" + line.split(':')[2]
    return books


def remove_book_from_file(book):
    books = {}

    file = open('books.txt', 'r')

    for line in file:
        if not line.split(":")[0] == book:
            books[line.split(':')[0]] = line.split(':')[1] + ":" + line.split(':')[2]

    file.close()

    file = open('books.txt', 'w')
    for i, j in books.items():
        file.write(i + ":" + j)


wanted_books = get_books_from_file()

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path="./geckodriver.exe")


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
            print("Ordered")
            ordered = True
            email_sending.send_email(book)
            remove_book_from_file(book)
            break
        except:  # Second try, for special reason: The td might be on another index
            try:
                i.find_elements_by_tag_name('td')[3].click()  # Try to click 'objednat odložení'
                driver.find_element_by_id('CC').send_keys('17753')  # Username
                driver.find_element_by_id('RC').send_keys('751115')  # Password

                driver.find_element_by_id('RC').send_keys(Keys.ENTER)
                print("Ordered")
                email_sending.send_email(book)
                remove_book_from_file(book)
                ordered = True
                break
            except:
                pass
    if not ordered:
        print("Not available")

driver.close()
