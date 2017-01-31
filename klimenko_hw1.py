import re

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

    def add_prof (self, txt):
        s = Prof()
        fio = s.get_fio(txt).split()
        surname = fio[0]
        name = fio[1]
        if len(fio) == 2:
            pat = None
        else:
            pat = fio[3]
        s.last_name = surname
        s.patronim = pat
        s.first_name = name
        s.place = get_place(txt)
        s.departament = get_dep(txt)
        s.mail = get_mail(txt)
        s.phone = get_phone(txt)
        s.interests = get_interest(txt)
        profs.append(s)

    def get_all_info(self):
        page = open('k.html', 'r', encoding='utf-8')
        f = page.read()
        pr = re.findall('<div class="post person">(.*?)<div class="post person">', f, flags=re.DOTALL)

    def get_mail(self, txt):
        m = re.search('mailto:(.*?)"', txt, flags=re.DOTALL)
        if m != '':
            return m
        else:
            return None

    def get_phone(self, txt):
        m = re.findall('<span>([доб\[0-9\] \-\(\)\+\.\*]*?)</span>', txt, flags=re.DOTALL)
        if m != '':
            return m
        else:
            return None

    def get_fio(self, txt):
        m = re.findall('title="(.*?)"', txt, flags=re.DOTALL)
        return m[0]

    def get_interest(self, txt):
        m = re.findall('href="https://www.hse.ru/org/persons/\?intst=.*?">(.*?)</a>', txt, flags=re.DOTALL)
        if m != '':
            return m
        else:
            return None

    def get_place(self, txt):
        all = []
        pr = re.findall('<p class="with-indent7">(.*?)</p>', txt, flags=re.DOTALL)
        for i in pr:
            k = re.findall('<span>(.*?)</span>', i, flags=re.DOTALL)
            for i in k:
                all.append(i)
            for j in all:
                who = (re.findall('([А-ЯЁа-яё, ]*?):', j, flags=re.DOTALL))
            return who[0]

    def get_dep(self, txt):
        all = []
        pr = re.findall('<p class="with-indent7">(.*?)</p>', txt, flags=re.DOTALL)
        for i in pr:
            k = re.findall('<span>(.*?)</span>', i, flags=re.DOTALL)
            for i in k:
                all.append(i)
            for j in all:
                dep = (re.findall('(>[А-ЯЁа-яё, ]*?)</a>', j, flags=re.DOTALL))
        return dep


page = open('k.html', 'r', encoding='utf-8')
f = page.read()
pr = re.findall('<div class="post person">(.*?)<div class="post person">', f, flags=re.DOTALL)
page.close()
for txt in pr:
    s = Prof()
    fio = s.get_fio(txt).split()
    surname = fio[0]
    name = fio[1]
    if len(fio) == 2:
        pat = None
    else:
        pat = fio[2]
    s.last_name = surname
    s.patronim = pat
    s.first_name = name
    s.place = s.get_place(txt)
    s.departament = s.get_dep(txt)
    s.mail = s.get_mail(txt)
    s.phone = s.get_phone(txt)
    s.interests = s.get_interest(txt)
    profs.append(s)