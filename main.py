import requests
from bs4 import BeautifulSoup


def get_html() -> list[str]:

    slovar_url: str = 'https://slovar.kakras.ru'
    txt_html: str = requests.get(slovar_url).text

    raw_html: list[str] = txt_html.split('\r\n')
    prep_html: list[str] = [item.strip() for item in raw_html if item != '']

    return prep_html


html_content: list[str] = get_html()

for html_line in html_content:
    if '<' not in html_line or '>' not in html_line:
        continue

    soup = BeautifulSoup(html_line, 'html.parser')

    start = soup.find(name='strong')

    if start:
        txt = start.next_sibling
        if txt is not None:
            print(txt)

#
# # start_words: element.ResultSet = soup.find_all(name='strong')
# # other_words: element.ResultSet = soup.find_all(name='b')
#

# for item in start_words:
#     print(type(item))

#
#
#     if ' ' not in word:
#         if word[8:-9].lower() not in all_words:
#             all_words.append(word[8:-9].lower())
#
# for item in other_words:
#     word = str(item)
#
#     if word == '<b>Яхонт</b>':
#         all_words.append(word[3:-4].lower())
#         break
#
#     elif ' ' not in word:
#         slice_word = word[3:-4]
#
#         slice_word = slice_word.replace('<u>', '')
#         slice_word = slice_word.replace('</u>', '')
#         slice_word = slice_word.replace('&lt;', '')
#         slice_word = slice_word.replace('&lt;', '')
#         slice_word = slice_word.replace('&gt;', '')
#         slice_word = slice_word.replace('!', '')
#         slice_word = slice_word.replace('?', '')
#
#         if slice_word.lower() not in all_words:
#             all_words.append(slice_word.lower())
#
# for _ in all_words:
#     print(_)