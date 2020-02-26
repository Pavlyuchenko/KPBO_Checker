import eel


def get_books_from_file():
    books = {}

    file = open('C:\\Users\\Michal\\Desktop\\books.txt', 'r')

    for line in file:
        books[line.split(':')[0]] = line.split(':')[1] + ":" + line.split(':')[2]
    return books


template = open('C:\\Users\\Michal\\Desktop\\template.txt', 'r',encoding="utf-8")
html = open('C:\\Users\\Michal\\Desktop\\result.html', 'w',encoding="utf-8")
books = get_books_from_file()

books_list = ""
for key, value in books.items():
    books_list += """
    <tr>
          <td>""" + key + """</td>
          <td><a href=""" + value + " target='_blank'>" + value + """</td>
    </tr>"""

for line in template:
    line = line.replace('{}', books_list)
    html.write(line)

template.close()
html.close()

eel.init('web')


@eel.expose
def save_book(book_name, url):
    file = open('C:\\Users\\Michal\\Desktop\\books.txt', 'r+')
    for line in file:
        pass
    file.write('\n' + book_name + ":" + url)
    file.close()

eel.start('result.html', size=(1000, 600), jinja_templates='web')
