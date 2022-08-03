import requests
from bs4 import BeautifulSoup

print('Type "en" if you want to translate from French into English, or "fr" if'
      'you want to translate from English into \French:')
target_lang = input()
if target_lang == 'en':
    translation_dir = 'french-english'
else:
    translation_dir = 'english-french'

print('Type the word you want to translate:')
word = input()

print(f'You chose "{target_lang}" as a language to translate "{word}".')

headers = {'User-Agent': 'Mozilla/5.0'}
while True:
    r = requests.get(f'https://context.reverso.net/translation/{translation_dir}/{word}', headers=headers)
    if r.status_code == 200:
        print(f'{r.status_code} OK')
        break

soup = BeautifulSoup(r.content, 'html.parser')

print('Translations')

# Translations
translations = []
for translation in soup.find_all('a', {'class': 'translation', 'class': 'ltr', 'class': 'dict'}):
    translations.append(translation.get('data-term'))
print(translations)

# Sentences
examples = []
for example in soup.find_all('div', {'class': 'src', 'class': 'ltr'}):
    # if not example.text.strip() == '':
    # print(example.parent.get('class')[0])
    if not example.parent.get('class') is None:
        if example.parent.get('class')[0] == 'example':
            examples.append(example.text.strip())
print(examples)

