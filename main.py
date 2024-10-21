import requests
from bs4 import BeautifulSoup

slovar_url: str = 'https://slovar.kakras.ru'
resptext: str = requests.get(slovar_url).text

soup: BeautifulSoup = BeautifulSoup(resptext, 'html.parser')

start_words: list[str] = soup.find_all(name='strong')
other_words: list[str] = soup.find_all(name='b')

all_words: list[str] = []

for item in start_words:
    word = str(item)

    if ' ' not in word:
        if word[8:-9].lower() not in all_words:
            all_words.append(word[8:-9].lower())

for item in other_words:
    word = str(item)

    if word == '<b>Яхонт</b>':
        all_words.append(word[3:-4].lower())
        break

    elif ' ' not in word:
        slice_word = word[3:-4]

        slice_word = slice_word.replace('<u>', '')
        slice_word = slice_word.replace('</u>', '')
        slice_word = slice_word.replace('&lt;', '')
        slice_word = slice_word.replace('&lt;', '')
        slice_word = slice_word.replace('&gt;', '')
        slice_word = slice_word.replace('!', '')
        slice_word = slice_word.replace('?', '')

        if slice_word.lower() not in all_words:
            all_words.append(slice_word.lower())

for _ in all_words:
    print(_)