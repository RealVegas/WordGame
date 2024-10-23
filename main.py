import re
import json
import requests
from random import randint
from pathlib import Path
from bs4 import BeautifulSoup, PageElement


# Получение html-кода с сайта
def get_html(dict_url: str) -> list[str]:

    # Запрос к сайту и получение html-кода
    txt_html: str = requests.get(dict_url).text

    # Разбиение html-кода на строки
    raw_html: list[str] = txt_html.split('\r\n')
    final_html: list[str] = [itm.strip() for itm in raw_html if '<' in itm and '>' in itm]

    return final_html


# Очистка слова
def clean_key(key_line: str) -> str:

    # Очистка конца строки от знаков препинания
    key_text: str = re.sub(r'[^а-яА-ЯёЁ]+$', '', key_line)

    # Удаление окончания строки после символов (,/ для исключения многозначных ответов
    key_text: str = re.sub(r'[(,/].*', '', key_text)

    # Большая первая буква в слове
    key_text: str = key_text[0].upper() + key_text[1:]

    return key_text.strip()


# Очистка описания слова
def clean_value(val_line: str) -> str:

    # Очистка начала строки от знаков препинания
    val_text: str = re.sub(r'^[^а-яА-ЯёЁ]+', '', val_line)

    if val_text == '':
        return ''

    # Удаление лишних пробелов
    val_text: str = ' '.join(val_text.split())

    # Удаление лишних слов
    # Не использовал регулярные выражения для удаления () иногда остающихся после удаления слов
    replace_words: list[str] = ['антилокус', 'Антилокус', 'локус', 'Локус', '()']
    for one_word in replace_words:
        val_text: str = val_text.replace(one_word, '')

    # Удаление конца строки после кавычки
    val_text: str = re.sub(r'».*', '', val_text)

    # Большая первая буква предложения
    val_text: str = val_text[0].upper() + val_text[1:]

    return val_text.strip()


# Заполнение игрового словаря
def create_dict(begin_tag: BeautifulSoup, empty_dict: dict[str, str]) -> None:
    val_text: str = ''

    # Обработка слова и получение описания слова
    key_text: str = clean_key(str(begin_tag.text))
    val_elem: PageElement | None = begin_tag.next_sibling

    # Если описание имеется обработка описания
    if val_elem is not None:
        val_text = clean_value(str(val_elem))

    # Если после обработки слово и описание не стали пустыми строками - запись в словарь
    if key_text != '' and val_text != '':
        empty_dict[key_text] = val_text

    return


# Разбиение текста на строки по максимальному количеству символов
def multi_text(txt: str, max_len: int) -> list[str]:

    # Разбиение текста на строки
    split_list: list[str] = txt.split()

    # Текущая строка и список строк
    current_line: str = ''
    result_list: list[str] = []

    # Формирование строк из слов с проверкой длины
    for one_word in split_list:

        if len(current_line) + len(one_word) + 1 <= max_len:

            if current_line == '':
                current_line = one_word
            else:
                current_line += ' ' + one_word

        else:
            result_list.append(current_line)
            current_line = one_word

    # Добавление последней строки
    if current_line:
        result_list.append(current_line)

    return result_list


# Парсинг сайта, заполнение игрового словаря
# количество и пропуск строк связаны со спецификой kakras.ru (парсер не универсальный)
def parse_site() -> dict[str, str]:

    game_dict: dict[str, str] = {}

    html_content: list[str] = get_html('https://slovar.kakras.ru')
    curr_line: int = 0

    while curr_line < 460:

        curr_line += 1
        html_line: str = html_content[curr_line]

        soup: BeautifulSoup = BeautifulSoup(html_line, 'html.parser')

        if curr_line == 319:
            continue

        elif curr_line < 40:
            s_tag: BeautifulSoup = soup.find(name='strong')
            if s_tag:
                create_dict(s_tag, game_dict)

        elif curr_line > 40:
            b_tag: BeautifulSoup = soup.find(name='b')
            if b_tag:
                create_dict(b_tag, game_dict)

    return game_dict


# Проверка наличия json-файла с игровым словарем
def verify_file() -> bool:
    file_path: Path = Path('game_resource.json')

    if file_path.is_file():
        return True
    else:
        return False


# Управление json-файлами

# Чтение json
def json_reader() -> dict[str, str]:

    file_path: Path = Path('game_resource.json')

    with open(file_path, mode='r', encoding='utf-8') as json_file:
        json_dict = json.load(json_file, ensure_ascii=False)

    json_deserial = json.loads(json_dict, ensure_ascii=False)
    return json_deserial


# Запись json
def json_writer(game_dict: dict[str, str]) -> None:

    json_serial = json.dumps(game_dict, ensure_ascii=False, indent=4)

    file_path: Path = Path('game_resource.json')
    with open(file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_serial, json_file, ensure_ascii=False, indent=4)

    return


# Запуск игры
def start_game() -> None:

    print('\nИгра: Угадай старинное слово\n')

    # Загрузка игрового словаря
    parsed_dict: dict[str, str] = json_reader()

    # Верхний предел для случайного выбора описания
    upper_bound = len(parsed_dict) - 1

    # Подсчет правильных и неправильных ответов
    win_score = 0
    loss_score = 0

    while True:

        random_item = randint(0, upper_bound)
        value_text = str(list(parsed_dict.values())[random_item])
        answer_text = str(list(parsed_dict.keys())[random_item])

        if len(value_text) > 100:
            value_text = multi_text(value_text, 100)
            for _ in value_text:
                print(_)
        else:
            print(value_text)

        print()
        user_answer = input('Введите загаданное слово или 0 если хотите закончить игру: ')

        if user_answer == '0':
            print(f'Загаданное слово: {answer_text}. Вы дали {win_score} правильных ответов и {loss_score} - неправильных\n')
            break

        elif user_answer.lower() == answer_text.lower():
            win_score += 1
            print(f'Верно! Правильных ответов: {win_score}: Неправильных ответов: {loss_score}\n')
        else:
            loss_score += 1
            print(f'Неверно! Правильный ответ: {answer_text}. Правильных ответов: {win_score}: Неправильных ответов: {loss_score}\n')


# Начальное меню и описание игры
def game_manager():

    # Введение
    print('Здравствуйте!\n')
    print('Сегодня в лёгкой игровой форме мы с Вами')
    print('Узнаем некоторые старинные слова и даже пару пословиц\n')

    if verify_file():

        print('Файл с игровым словарем найден\n')
        print('+--------------------------------------+')
        print('| 1. Начать игру                       |')
        print('| 2. Распарсить сайт: slovar.kakras.ru |')
        print('+--------------------------------------+\n')

        request = input('Выберите действие: ')

        if request == '1':
            start_game()
        else:
            temp_dict = parse_site()
            print('\nСайт: slovar.kakras.ru успешно распасен\n')
            save_request = input('Вы хотите сохранить данные с сайта? (y/n): ')

            if save_request == 'y':
                json_writer(temp_dict)
                print('\nФайл успешно сохранен')
                print('+--------------------------------------+')
                print('| Если вы хотите изменить слова или    |')
                print('| дополнить список слов, изменить или  |')
                print('| описания слов,вам необходимо         |')
                print('| отредактировать файл:                |')
                print('| game_resource.json                   |')
                print('+--------------------------------------+\n')

                game_request = input('Ну что, будете играть? (y/n): ')

                if game_request == 'y':
                    start_game()
    else:
        print('Файл с игровым словарем не найден\n')
        print('Придется распарсить сайт и сохранить данные\n')
        save_request = input('Начнём? (y/n): ')

        if save_request == 'y':
            temp_dict = parse_site()
            print('\nСайт: slovar.kakras.ru успешно распасен\n')

            json_writer(temp_dict)
            print('\nФайл успешно сохранен')
            print('+--------------------------------------+')
            print('| Если вы хотите изменить слова или    |')
            print('| дополнить список слов, изменить или  |')
            print('| описания слов,вам необходимо         |')
            print('| отредактировать файл:                |')
            print('| game_resource.json                   |')
            print('+--------------------------------------+\n')

            game_request = input('Ну что, будете играть? (y/n): ')

            if game_request == 'y':
                start_game()