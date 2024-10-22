import re
import requests
from random import choice
from bs4 import BeautifulSoup


def clean_string(line: str) -> str:
    text: str = re.sub(r'^[^а-яА-ЯёЁ]+', '', line).strip()

    if text == '':
        return ''

    text: str = ' '.join(text.split())

    forbidden_words: list[str] = ['антилокус', 'Антилокус', 'локус', 'Локус', '()']

    for item in forbidden_words:
        text = text.replace(item, '')

    closing_quote: int = text.find('»', 1)
    if closing_quote != -1:
        text: str = text[:closing_quote + 1]

    text = text[0].upper() + text[1:]

    return text


def clean_words(word: str) -> str:
    clean = word.replace('«', '')
    clean = word.replace('»', '')

    clean = re.sub(r'[^а-яА-ЯёЁ]+$', '', word)

    open_bracket: int = clean.find('(', 1)
    if open_bracket != -1:
        clean: str = clean[:open_bracket]

    comma_pos: int = clean.find(',', 1)
    if comma_pos != -1:
        clean: str = clean[:comma_pos]

    slash_pos: int = clean.find('/', 1)
    if slash_pos != -1:
        clean: str = clean[:slash_pos]

    clean = clean[0].upper() + clean[1:]

    clean = clean.strip()

    return clean


def get_html() -> list[str]:
    slovar_url: str = 'https://slovar.kakras.ru'
    txt_html: str = requests.get(slovar_url).text

    raw_html: list[str] = txt_html.split('\r\n')
    prep_html: list[str] = [item.strip() for item in raw_html if '<' in item and '>' in item]

    return prep_html


html_content: list[str] = get_html()
curr_line = 0

while curr_line < 460:

    curr_line += 1
    html_line = html_content[curr_line]

    soup = BeautifulSoup(html_line, 'html.parser')

    if curr_line == 319:
        continue

    elif curr_line < 40:
        start = soup.find(name='strong')
        if start:
            txt = start.next_sibling
            if txt is not None and clean_string(str(txt)) != '':
                print(f'{curr_line} | {clean_words(str(start.text))} : {clean_string(str(txt))}')

    elif curr_line > 40:
        start = soup.find(name='b')
        if start:
            txt = start.next_sibling
            if txt is not None and clean_string(str(txt)) != '':
                print(f'{curr_line} | {clean_words(str(start.text))} : {clean_string(str(txt))}')