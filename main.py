from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import test

wanted_books = {
    'Algor, Mráz a hry': 'https://www.okpb.cz/clavius/l.dll?cll~P=276922',
    'Karotsský gambit': 'https://www.okpb.cz/clavius/l.dll?cll~P=1260300',
    'Jméno větru': 'https://www.okpb.cz/clavius/l.dll?cll~P=223432',
    'Ideální investiční portfolio': 'https://www.okpb.cz/clavius/l.dll?cll~P=2527349',
    'Začínáme na burze': 'https://www.okpb.cz/clavius/l.dll?cll~P=1659855',
    'Kronika sci-fi': 'https://www.okpb.cz/clavius/l.dll?cll~P=430248',
    'Resturant na konci vesmíru': 'https://www.okpb.cz/clavius/l.dll?cll~P=283832',
}

print("Running")

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path="./geckodriver.exe", options=options)

for book in wanted_books.keys():
    ordered = False
    driver.get(wanted_books[book])  # Choose each book from dictionary
    table_rows = driver.find_elements_by_xpath('//tr')  # Find ALL table row elements
    potentional_free_books = []  # List for books in Dospělí, Mládež and Kateřinky
    for i in table_rows:  # For each table row
        try:
            valid = i.find_element_by_class_name('SVSL1')  # If you find table row that stands for some oddělení
            if valid.text == "  " or valid.text == " M/III " or valid.text == " KA ":  # Then check if it is one of my possible oddělení
                potentional_free_books.append(i)  # If the two upper conditions are met, add it to the list
        except:
            pass

    for i in potentional_free_books:  # For each potential free book
        try:
            i.find_elements_by_tag_name('td')[4].click()  # Try to click 'objednat odložení'
            driver.find_element_by_id('CC').send_keys('17753')  # Username
            driver.find_element_by_id('RC').send_keys('751115')  # Password
            import time
            time.sleep(2)
            driver.find_element_by_id('RC').send_keys(Keys.ENTER)  # Confirm
            print("Ordered")  # To-Do: Email
            ordered = True
            break
        except:  # Second try, for special reason: The td might be on another index
            try:
                i.find_elements_by_tag_name('td')[3].click()  # Try to click 'objednat odložení'
                driver.find_element_by_id('CC').send_keys('17753')  # Username
                driver.find_element_by_id('RC').send_keys('751115')  # Password
                import time

                time.sleep(2)
                driver.find_element_by_id('RC').send_keys(Keys.ENTER)
                print("Ordered")  # To-Do: Email
                ordered = True
                break
            except:
                pass
    if not ordered:
        print("Not available")

driver.close()
print("Finished")
