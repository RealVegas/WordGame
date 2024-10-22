import re
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


def clean_string(line: str) -> str:
    text: str = re.sub(r'^[^а-яА-ЯёЁ]+', '', line).strip()

    if text == '':
        return ''

    text: str = ' '.join(text.split())

    forbidden_words: list[str] = ['антилокус', 'Антилокус', 'локус', 'Локус', '()']

    for itm in forbidden_words:
        text: str = text.replace(itm, '')

    closing_quote: int = text.find('»', 1)
    if closing_quote != -1:
        text: str = text[:closing_quote + 1]

    text: str = text[0].upper() + text[1:]

    return text


def clean_words(word: str) -> str:
    clean: str = re.sub(r'[^а-яА-ЯёЁ]+$', '', word)

    open_bracket: int = clean.find('(', 1)
    if open_bracket != -1:
        clean: str = clean[:open_bracket]

    comma_pos: int = clean.find(',', 1)
    if comma_pos != -1:
        clean: str = clean[:comma_pos]

    slash_pos: int = clean.find('/', 1)
    if slash_pos != -1:
        clean: str = clean[:slash_pos]

    clean: str = clean[0].upper() + clean[1:]

    clean: str = clean.strip()

    return clean


def fill_dictionary(begin_tag: BeautifulSoup, fill_dict: dict[str, str]) -> None:
    meaning: str = ''

    olden_word: str = clean_words(str(begin_tag.text))
    mean_text: PageElement | None = begin_tag.next_sibling

    if mean_text is not None:
        meaning = clean_string(str(mean_text))

    if olden_word != '' and meaning != '':
        fill_dict[olden_word] = meaning


def get_html() -> list[str]:
    dictionary_url: str = 'https://slovar.kakras.ru'
    txt_html: str = requests.get(dictionary_url).text

    raw_html: list[str] = txt_html.split('\r\n')
    prep_html: list[str] = [itm.strip() for itm in raw_html if '<' in itm and '>' in itm]

    return prep_html


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