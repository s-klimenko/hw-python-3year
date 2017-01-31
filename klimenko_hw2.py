import requests
from lxml import html # для xpath импортируем html
from lxml import etree

profs = []

class Prof: # у всех функций внутри класса первый аргумент self
    def __init__(self): #волшебная функция, прописать все свойства
        self.last_name = ''
        self.patronim = ''
        self.first_name = ''
        self.place = []
        self.departament = []
        self.mail = ''
        self.phone = []
        self.interests = []

def mail_lego(mails): #собирает из зашифрованного email нормальный
    mail_built = []
    for mail in mails:
        mail_b = mail.replace('-at-', '@').replace('["', '').replace('","', '').replace('"]', '')
        mail_built.append(mail_b)
    return mail_built


def prof_maker(profs, name, phones, mails, place_cut, departament, interest): #делает из данных объект класса и вкладывает его в список
    s = Prof()
    fio = name[0].split(' ')
    surname = fio[0]
    name = fio[1]
    if len(fio) == 2:
        pat = None
    else:
        pat = fio[2]
    s.last_name = surname
    s.patronim = pat
    s.first_name = name
    s.place = place_cut
    s.departament = departament
    s.mail = mail_lego(mails)
    s.phone = phones
    s.interests = interest
    profs.append(s)

def xpath_profs(page): #возвращает список созданный xpath
    profs = []
    tree = html.fromstring(page.content) # в этом месте парсер построил дерево элементов
    persons = tree.xpath('//div[@class="post__content post__content_person"]')
    # собираем список дат
    for per in persons:
        place_cut = []
        phones = per.xpath('.//div[@class="l-extra small"]/span/text()')
        mails = per.xpath('.//div[@class="l-extra small"]/a/@data-at')
        name = per.xpath('.//div[@class="g-pic person-avatar-small2"]/@title')
        places = per.xpath('.//p[@class="with-indent7"]/span/text()')

        for place in places:
            place = place.strip()
            if place != '' and not place.startswith('/'):
                place_cut.append(place)

        departament = per.xpath('.//p[@class="with-indent7"]/span/a[@class="link"]/text()')
        interest = per.xpath('.//div[@class="with-indent small"]/a/text()')
        prof_maker(profs, name, phones, mails, place_cut, departament, interest)
    return profs


def etree_profs(page): #возвращает список созданный etree
    profs = []
    root = etree.HTML(page.content)
    persons = root[1][1][3][2][1][0][2][1]
    for pers in persons:
        name = []
        per = pers[0][0]
        phones = []
        place_cut = []
        departament = []
        interest = []
        mails = []

        if 'l-extra small' in per.attrib['class']:
            for part in per:
                if part.tag == 'span':
                    phone = part.text
                    phones.append(phone)
                if part.tag == 'a':
                    mail = part.get('data-at')
                    mails.append(mail)
            per = pers[0][1]

        if 'main content small' in per.attrib['class']:
            name.append(per[0][0][0].get('title')) #почему-то не сработал .text
            dep_pl = per[0][1]
            for i in dep_pl:
                if i.tag == 'span':
                    pl = i.text.strip()
                    place_cut.append(pl)
                    for d in i:
                        dep = d.text.strip()
                        departament.append(dep)
            if len(per[0]) == 3:
                ints = per[0][2]
                for child in ints:
                    intr = child.text.strip()
                    interest.append(intr)

        prof_maker(profs, name, phones, mails, place_cut, departament, interest)
    return profs

page = requests.get('https://www.hse.ru/org/persons/?ltr=%D0%A0;udept=22726')
print('Список фамилий из xpath:')
for i in xpath_profs(page):
    print(i.last_name)
print('\n', 'Список фамилий из etree:')
for i in etree_profs(page):
    print(i.last_name)
print('\n', 'end')
