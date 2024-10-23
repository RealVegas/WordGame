import re
import json
import requests
from random import randint
from bs4 import BeautifulSoup, PageElement


def split_string(text: str, max_length: int) -> list[str]:
    split_text: list[str] = text.split()

    current_line: str = ''
    lines: list[str] = []

    for one_word in split_text:

        if len(current_line) + len(one_word) + 1 <= max_length:
            if current_line == '':
                current_line = one_word
            else:
                current_line += ' ' + one_word
        else:
            lines.append(current_line)
            current_line = one_word

    if current_line:
        lines.append(current_line)

    return lines


def get_html() -> list[str]:
    dict_url: str = 'https://slovar.kakras.ru'
    txt_html: str = requests.get(dict_url).text

    raw_html: list[str] = txt_html.split('\r\n')
    final_html: list[str] = [itm.strip() for itm in raw_html if '<' in itm and '>' in itm]

    return final_html

def clean_key(key_line: str) -> str:

    # Очистка конца строки от знаков препинания
    key_text: str = re.sub(r'[^а-яА-ЯёЁ]+$', '', key_line)

    # Удаление окончания строки после символов (,/ для исключения многозначных ответов
    key_text: str = re.sub(r'[(,/].*', '', key_line)

    # Большая первая буква в слове
    key_text: str = key_text[0].upper() + key_text[1:]

    return key_text.strip()

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













def fill_dictionary(begin_tag: BeautifulSoup, fill_dict: dict[str, str]) -> None:
    meaning: str = ''

    olden_word: str = clean_words(str(begin_tag.text))
    mean_text: PageElement | None = begin_tag.next_sibling

    if mean_text is not None:
        meaning = clean_string(str(mean_text))

    if olden_word != '' and meaning != '':
        fill_dict[olden_word] = meaning








parsed_dictionary: dict[str, str] = {}

html_content: list[str] = get_html()
curr_line: int = 0

while curr_line < 460:

    curr_line += 1
    html_line: str = html_content[curr_line]

    soup: BeautifulSoup = BeautifulSoup(html_line, 'html.parser')
    find_tag: None = None

    if curr_line == 319:
        continue

    elif curr_line < 40:
        strong_tag: BeautifulSoup = soup.find(name='strong')
        if strong_tag:
            fill_dictionary(strong_tag, parsed_dictionary)

    elif curr_line > 40:
        b_tag: BeautifulSoup = soup.find(name='b')
        if b_tag:
            fill_dictionary(b_tag, parsed_dictionary)

# Game

print('Игра: Угадай старинное слово\n')

upper_bound = len(parsed_dictionary) - 1
right_score = 0
wrong_score = 0

while True:

    random_number = randint(0, upper_bound)
    word_mean = list(parsed_dictionary.values())[random_number]

    if len(word_mean) > 100:
        word_mean = split_string(word_mean, 100)

    if type(word_mean) is list:
        for _ in word_mean:
            print(_)
    else:
        print(word_mean)

    print()

    user_answer = input('Введите загаданное слово или 0 если Вы хотите закончить игру: ')
    right_answer = str(list(parsed_dictionary.keys())[random_number])

    if user_answer == '0':
        print(f'Загаданное слово: {right_answer}. Вы дали {right_score} правильных ответов и {wrong_score} - неправильных\n')
        break

    elif user_answer.lower() == right_answer .lower():
        right_score += 1
        print(f'Верно! Правильных ответов: {right_score}: Неправильных ответов: {wrong_score}\n')
    else:
        wrong_score += 1
        print(f'Неверно! Правильный ответ: {right_answer}. Правильных ответов: {right_score}: Неправильных ответов: {wrong_score}\n')