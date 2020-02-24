import eel

eel.init('web')


@eel.expose
def save_book(book_name, url):
    file = open('books.txt', 'r+')
    for line in file:
        pass
    file.write('\n' + book_name + ":" + url)
    file.close()


eel.start('index.html', size=(1000, 600))
