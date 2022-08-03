import requests
from bs4 import BeautifulSoup

print('Type "en" if you want to translate from French into English, or "fr" if'
      'you want to translate from English into \French:')
target_lang = input()
if target_lang == 'en':
    translation_dir = 'french-english'
else:
    translation_dir = 'english-french'
target_lang_full = translation_dir[:translation_dir.find('-')]

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

print(f'{target_lang_full.capitalize()} Translations')

# Translations
translations = []
for translation in soup.find_all('a', {'class': 'translation', 'class': 'ltr', 'class': 'dict'}):
    translations.append(translation.get('data-term'))
    print(translations[-1])

# Sentences
print(f'\n{target_lang_full.capitalize()} Examples')
examples = []
for example in soup.find_all('div', {'class': 'src ltr'}):
    if not example.parent.get('class') is None:
        if example.parent.get('class')[0] == 'example':
            examples.append([example.text.strip(), ''])

i = 0
for example_trg in soup.find_all('div', {'class': 'trg ltr'}):
    if not example_trg.parent.get('class') is None:
        if example_trg.parent.get('class')[0] == 'example':
            examples[i][1] = example_trg.text.strip()

            print(examples[i][0])
            print(examples[i][1])
            print()
            i = i + 1

