from pymystem3 import Mystem  # импортируем майстем
import requests
import json
import re
from verbs import lemma_counter


def check_error_vkAPI(response):

    response = response.json()
    if 'error' in response.keys():
        if response['error']['error_code'] == 15:
            error = 'Отказано в доступе. Пожалуйста, введите ID открытого сообщества. :)'
        elif response['error']['error_code'] == 100:
            error = 'Ошибка в написании ID. Пожалуйста, введите ID еще раз, это должно быть положительное число. :)'
        elif response['error']['error_code'] == 18:
            error = 'Группа удалена, забанена или еще не существует. Пожалуйста, введите ID другой группы. :)'
        else:
            error = 'Error message: %s. Error code: %s' % \
                    (response['error']['error_msg'], response['error']['error_code'])
    else:
        error = False
    return error


def clean_html(raw_html):
    clean_r = re.compile('<.*?>')
    clean_text = re.sub(clean_r, '', raw_html)
    return clean_text


def count_words(posts, needed_pos=None):
    m = Mystem()  # создаем экземпляр класса-анализатора
    ana = m.analyze(posts)
    words = [i['analysis'][0] for i in ana if i['text'].strip() and 'analysis' in i and i['analysis']]
    if needed_pos is not None:
        words = [i for i in words if i['gr'].split('=')[0].split(',')[0] in needed_pos]
    return lemma_counter(words)

def get_vk_posts(id_vk):
    '''
    Функция скачивает первые 1000 постов со стены группы (если постов меньше 1000, то скачивает все) и возвращает одной строкой. Если группа закрытая, возвращает ошибку.
    :param id_vk: ID руппы
    :type id_vk: int
    :return:
    :rtype
    '''
    all_posts = ''
    response = requests.get('https://api.vk.com/method/wall.get?owner_id=-{}&count=1'.format(str(id_vk)))
    error_text = check_error_vkAPI(response)
    if not error_text:
        for offset in range(0, 1001, 100):
            print(offset)
            response = requests.get('https://api.vk.com/method/wall.get?owner_id=-{}&count=10&offset={}'
                                    .format(id_vk, str(offset)))
            data = json.loads(response.text)
            for i in range(1, len(data['response'])):
                all_posts += clean_html(data["response"][i]["text"])
    else:
        error_message = True
        return error_message, error_text
    error_message = False
    result = count_words(all_posts, ['V', 'N', 'ADV', 'A'])
    return error_message, result
