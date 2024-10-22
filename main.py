import re
import requests
from random import choice
from bs4 import BeautifulSoup, PageElement


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

curr_line = 0

for item, item_meaning in parsed_dictionary.items():
    curr_line += 1
    print(f'{curr_line} | {item} : {item_meaning}')